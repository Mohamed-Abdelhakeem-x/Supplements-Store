from flask import flask, render_template

app = flask(__name__)

@app.route("/")
@app.route("/Home")

def index():
    return "Welcome to home page"

@app.route("/About")
def about():
    return "Welcome to about page"

@app.route("/Shop")
def Shop():
    return "Welcome to Shopping page"

@app.route("/Hot-Deals")
def Hot_Deals():
    return "Welcome to Hot Deals page"

if __name__ == "__main__":
    app.run()