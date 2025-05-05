from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "subject <h1> HEADING <h1>"

@app.route("/<name>")
def user(name):
    return f"this is called : {name}"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()