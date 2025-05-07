from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form["nm"] == "aiwan":
            return(redirect(url_for("admin")))
        
        else:
            user = request.form["nm"]
            session["user"] = user
            return redirect(url_for("user", name = user))
    else:
        return render_template("login.html")
    

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("name.html", name = user)
    else:
        return redirect(url_for("login"))
    
    

@app.route("/admin")                 
def admin():
    return redirect(url_for("user", name = "ADMIN"))

if __name__ == "__main__":
    app.run(debug = True)