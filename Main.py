from flask import Flask, render_template , redirect, url_for, flash
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '124pofds12h413knf13pomo5'


@app.route('/')
@app.route("/Home", methods=['GET','POST'])
def Home():
    return render_template('Home.HTML', title = "Home", cssFile = "Static/css/Home.css")

@app.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "Static/css/About.css")

@app.route("/Shop")
def Shop():
    return render_template('Shop.HTML', title = "Shop", cssFile = "Static/css/Shop.css")

@app.route('/login', methods=['GET','POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       if form.email.data == "admin" and form.password.data == "admin":
            flash("Form submitted successfully!", "success")
            return redirect(url_for("Home"))
       else:
            flash("Invalid email or password.", "danger")
   return render_template('login.HTML', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
      flash(f"Account created for {form.username.data}!", "success")
      return redirect(url_for("login"))
   
   return render_template('signup.HTML',form=form)

if __name__ == "__main__":
    app.run(debug=True,port=3000)