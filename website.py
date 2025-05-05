from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<name>")
def user(name):
    return render_template("name.html", name = name)

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = "admin"))

if __name__ == "__main__":
    app.run(debug = True)