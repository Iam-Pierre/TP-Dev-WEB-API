from pyexpat import features

from flask import Blueprint, request, session, g, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import pickle

from extensions import db
from models import User, ApiKey

from models_ml import rf_model, feature_names, shap_explainer


api = Blueprint("api", __name__)


def login_required(f):
    """
        session uniquement

        grace à la variable g.user, on peut accéder à l'utilisateur connecté 
        dans les fonctions de route protégées par ce décorateur
    """
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return {"error": "non autorisé"}, 401

        user = User.get_by_username(session["user"])
        if user is None:
            session.clear()
            return {"error": "non autorisé"}, 401

        g.user = user
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def auth_required(f):
    """
        session ou clé API
        
        grace à la variable g.user, on peut accéder à l'utilisateur connecté 
        dans les fonctions de route protégées par ce décorateur
    """
    def wrapper(*args, **kwargs):
        user = None

        if "user" in session:
            user = User.get_by_username(session["user"])

        if user is None:
            api_key_header = request.headers.get("X-API-Key")
            if api_key_header is not None:
                api_key = ApiKey.get_by_key(api_key_header)
                if api_key is not None:
                    user = api_key.user

        if user is None:
            return {"error": "non autorisé"}, 401

        g.user = user
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper



#######################
##### ROUTE LOGIN #####
#######################

@api.route("/api/login", methods=["POST"])
def handleLogin():
    data = request.get_json()

    u = data.get("username", None)
    p = data.get("password", None)

    user = User.get_by_username(u)

    if user is None:
        return {"error": "utilisateur ou mot de passe incorrect"}, 401
    
    if not check_password_hash(user.password_hash,p):
        return {"error": "utilisateur ou mot de passe incorrect"}, 401
    
    session["user"] = u 
    return {"ok": True}


@api.route("/api/register", methods=["POST"])
def handleRegister():
    data = request.get_json()

    u = data.get("username","")
    p = data.get("password","")

    if User.get_by_username(u) is not None:
        return {"error": "Nom d'utilisateur déja pris"}, 400
    
    new_user = User(username = u, password_hash = generate_password_hash(p))
    db.session.add(new_user)
    db.session.commit()

    session["user"] = u
    return {"ok": True}

    
@api.route("/api/logout", methods=["POST"])
@login_required
def handleLogout():
    session.clear()
    return {"ok": True}

###########################
##### ROUTE DASHBOARD #####
###########################



@api.route("/api/keys/<int:key_id>", methods=["DELETE"])
@login_required
def delete_key(key_id):
    key = ApiKey.query.filter_by(id=key_id, user_id=g.user.id).first()

    db.session.delete(key)
    db.session.commit()
    return {"ok": True}


@api.route("/api/keys", methods=["POST"])
@login_required
def create_key():

    try:
        data = request.get_json()

        a = data.get("apiName","")
        u = g.user

        raw_key, api_key = ApiKey.new(u,a)
        g.user.consume_quota()


        # print([key.label for key in g.user.api_keys]) Utilise pour lire les clé de l'utilisateur dans la console

        return {"raw_key": raw_key, "id": api_key.id, "label": api_key.label}
    except:
        return {"error": "Erreur clé API non créée"}, 403
    
####################
#### ROUTE APP #####
####################

@api.route("/api/predict", methods=["POST"])
@auth_required
def predict():
    data = request.get_json()
    features = [float(data[f]) for f in feature_names]
    prediction = rf_model.predict_proba([features])[0][1]
    return {"proba": prediction}

@api.route("/api/waterfall", methods=["GET"])
@auth_required
def waterfall():
    import shap
    import matplotlib.pyplot as plt
    from io import BytesIO
    from flask import send_file
    import numpy as np

    features = np.array([[float(request.args.get(f)) for f in feature_names]])
    shap_values = shap_explainer.shap_values(features)
    
    explanation = shap.Explanation(
        values=shap_values[0][0],
        base_values=float(shap_explainer.expected_value[0]),
        data=features[0],
        feature_names=feature_names
    )
    
    shap.plots.waterfall(explanation, max_display=len(feature_names), show=False)
    
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    
    return send_file(buf, mimetype="image/png")

