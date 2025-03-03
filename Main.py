from flask import Flask, render_template , redirect, url_for, flash
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sajdpfj apsosa fposkaf'

@app.route('/')
@app.route("/Home")
def index():
    return render_template('index.HTML', title = "Home", cssFile = "Static/css/main.css")

@app.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "Static/css/About.css")

@app.route("/Shop")
def Shop():
    return render_template('Shop.HTML', title = "Shop", cssFile = "Static/css/Shop.css")

@app.route("/Hot-Deals")
def Hot_Deals():
    return render_template('Hot-Deals.HTML', title = "Hot Deals", cssFile = "Static/css/Hot-Deals.css")

@app.route('/login', methods=['GET','POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
         flash('Login Successfully', 'success')
         return redirect(url_for('home'))
            
   return render_template('login.html', title="Login", form=form, cssFile = "Static/css/Login.css")

@app.route('/register', methods=['GET','POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
      flash('Account Created', 'success')
      return redirect(url_for('home'))
   
   return render_template('register.html', title="Sign up",form=form, cssFile = "Static/css/signup.css")

if __name__ == "__main__":
    app.run(debug=True,port=3000)