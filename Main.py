from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods = ['GET'])
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

def login():
   form = LoginForm()
   if form.validate_on_submit():
      if form.email.data == "abdo@gmail.com" and form.password.data == "123456":
         flash('Login Successfully', 'success')
         return redirect(url_for('home'))
      else:
         flash('Invalid Credential', 'danger')
   return render_template('login.html', title="Login", form=form)

@app.route('/register', methods=['GET','POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
      flash('Account Created', 'success')
      return redirect(url_for('home'))
   
   return render_template('register.html', title="Sign up",form=form)

if __name__ == "__main__":
    app.run(debug=True,port=3000)