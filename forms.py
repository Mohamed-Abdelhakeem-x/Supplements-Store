from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    phone = StringField('Mobile Number', validators=[DataRequired(), Length(min=11,max=11)])
    password =  PasswordField('Password', validators=[DataRequired(),Length(min=6)])
    confirm_password =  PasswordField('Confrim Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Signup')
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    login = SubmitField("Login")

class CartForm(FlaskForm):
    title = StringField('Item Name', validators=[DataRequired()])
    submit = SubmitField('Add Order')

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField('Your Review', validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField('Post Review')