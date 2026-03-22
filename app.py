from flask import Flask, render_template, session, redirect
import pickle
from extensions import db, sess
from models import User
from routes import api
import jinja2


app = Flask(__name__)

with open("models/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)


app.config["SECRET_KEY"] = "dev-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = db

db.init_app(app)
sess.init_app(app)

app.register_blueprint(api)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    username = session.get("user",None)
    if username is not None:
        return render_template("app.html",FEATURES=feature_names)
    return render_template("auth.html")

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session.get("user",None)
    if username is not None:
        return render_template("dashboard.html", user=User.get_by_username(username))
    return redirect("/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)