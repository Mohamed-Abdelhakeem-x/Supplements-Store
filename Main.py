from flask import Flask, render_template , redirect, url_for, flash
from forms import RegisterForm, LoginForm, CartForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '124pofds12h413knf13pomo5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

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

@app.route('/Cart', methods=['GET', 'POST'])
def add_task():
    form = CartForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data, completed=form.completed.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks_list'))
    return render_template('Cart.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       if form.email.data == "mohamed.abdelhakeem@gmail.com" and form.password.data == "123456":
            flash("Logged in successfully!", "success")
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
   else:
         flash('Invalid Credential', 'danger')
   return render_template('signup.HTML',form=form)

if __name__ == "__main__":
    app.run(debug=True,port=3000)