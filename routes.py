from flask import Blueprint, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User, ApiKey


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
def login():
    #a vous d'ecrire le code
    return {"error": "non implementer"}, 501


@api.route("/api/register", methods=["POST"])
def register():
    #a vous d'ecrire le code
    return {"error": "non implementer"}, 501

@api.route("/api/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return {"ok": True}

###########################
##### ROUTE DASHBOARD #####
###########################

@api.route("/api/keys/<int:key_id>", methods=["DELETE"])
@login_required
def delete_key(key_id):
    """
    supprime la clé API spécifiée (si elle appartient à l'utilisateur connecté)
    """
    #a vous d'ecrire le code
    return {"error": "non implementer"}, 501

@api.route("/api/keys", methods=["POST"])
@login_required
def create_key():
    """
    crée une nouvelle clé API pour l'utilisateur connecté avec un label spécifié
    retourne la clé API générée
    """
    #a vous d'ecrire le code
    return {"error": "non implementer"}, 501



####################
#### ROUTE APP #####
####################

@api.route("/api/predict", methods=["POST"])
@auth_required
def predict():
    #la fonction predict de votre TP
    return {"error": "non implementer"}, 501

@api.route("/api/waterfall", methods=["GET"])
@auth_required
def waterfall():
    #la fonction waterfall de votre TP
    return {"error": "non implementer"}, 501