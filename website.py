from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(hours=5)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_info.db"
db = SQLAlchemy(app)
class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["nm"]
        email = request.form["em"]

        # Check if user exists in the database
        user_found = users.query.filter_by(name=username).first()

        if user_found:
            flash("Account already found")
            # Use the found user to store session data
            session["user"] = user_found.name
            session["email"] = user_found.email
        
        else:
            # Create new user if not found
            usr = users(name=username, email=email)
            db.session.add(usr)
            db.session.commit()
            flash("New account created")
            session["user"] = username
            session["email"] = email

        if username == "aiwan":
            session["user"] = "ADMIN"
            session["email"] = "testemail@gmail.com"
            flash("Login successfull!")
            return(redirect(url_for("admin")))
        
        else:
            session.permanent = True
            flash("Login successfull!")
            return redirect(url_for("user", name = username, email = email))
    else:
        if "user" in session:
            flash("You are already loged in")
            return redirect(url_for("user", name = session["user"]))
        return render_template("login.html")
    

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        email = session["email"]
        return render_template("name.html", name = user, email = email)
    else:
        return redirect(url_for("login"))
    

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("logout successfull!", "info")
    return redirect(url_for("login")) 

@app.route("/admin")                 
def admin():
    return redirect(url_for("user", name = "ADMIN", email = "testemail@gmail.com"))

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)