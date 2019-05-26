from flask import Flask,jsonify, render_template, redirect, url_for, session, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy

#other imports not part of full text search
from flask_bcrypt import Bcrypt

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets import TextArea
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import current_user
from flask_login import login_required
import flask_login
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os 

import random
import datetime




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hlkwywzjmhpcus:2a9c6870fe8bd3ebfbde742d4ec305f50ca5b500c603db486d28c6cc5cfe12fa@ec2-54-163-226-238.compute-1.amazonaws.com:5432/d2ln3vdh40uekt
'
app.config['SECRET_KEY'] = 'df12959f86353c9792509ecc5ae07940'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(120), nullable=False)
        lastname = db.Column(db.String(120), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
        maxPos = db.Column(db.Float())
        minPos = db.Column(db.Float())

        preference = db.Column(db.Integer())


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember Me?")
	submit = SubmitField("Login!")


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Register!")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("User Already Exists")

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()

		if email:
			raise ValidationError("Email Already Exists")

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/getPos/<id>')
def getPos(id):
    user = User.query.get(id)
    jsonUser = {
    "maxPos": user.maxPos,
    "minPos": user.minPos
            }
    return jsonify(jsonUser)

@app.route('/getPref/<id>')
def getPref(id):
    user = User.query.get(id)
    jsonUser = {
            "pref": user.preference}
    return jsonify(jsonUser)

@app.route('/login', methods=["POST", "GET"])
def login():
	imageUrl = url_for('static', filename="img/display_content/{0}.jpg".format(random.randint(1,9)))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data)
		print("-------------------------")
		print(user)

		if user == "":
			user = User.query.filter_by(username=form.email.data)
			print(user)

		user = user.first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):

			login_user(user)
			return redirect(url_for('index'))


	return render_template('login.html', form=form, imageUrl=imageUrl)

@app.route('/register', methods=["POST", "GET"])
def register():
	imageUrl = url_for('static', filename="img/display_content/{0}.jpg".format(random.randint(1,9)))
	form1 = RegistrationForm()


	if form1.validate_on_submit():
		print("got form")
		hashed_password = bcrypt.generate_password_hash(form1.password.data).decode("utf-8")
		user = User(username=form1.username.data, email=form1.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))

	return render_template('register.html',form1 = form1, imageUrl=imageUrl)

@app.route('/logout', methods=["GET", "POST"])
def logout():
	flask_login.logout_user()
	return redirect(url_for("index"))

if __name__ == "__main__":
	app.run()
