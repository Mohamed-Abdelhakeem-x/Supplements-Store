from flask import Flask, render_template

app = flask(__name__)

@app.route("/")
@app.route("/Home")
def index():
    return render_template('Home.HTML', title = "Home", cssFile = "main.css")

@app.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "About.css")

@app.route("/Shop")
def Shop():
    return render_template('Shop.HTML', title = "Shop", cssFile = "Shop.css")

@app.route("/Hot-Deals")
def Hot_Deals():
    return render_template('Hot-Deals.HTML', title = "Hot Deals", cssFile = "Hot-Deals.css")

if __name__ == "__main__":
    app.run()