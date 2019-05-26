from flask import Flask, render_template, redirect, url_for, session, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa


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

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qgusigivvhedfy:2d69d1a8d228f06a9edca3f6bc541ed7a8c42dde0d1d833613408e06bb0059b2@ec2-54-235-160-57.compute-1.amazonaws.com:5432/d7orn9jaelapdn"
app.config['SECRET_KEY'] = 'df12959f86353c9792509ecc5ae07940'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.Text, nullable=False)
	cosmosEmail = db.Column(db.String(120),unique=True)

class Judge(db.Model):
	__tablename__ = "judge"
	__searchable__ = ['firstname', 'lastname', 'paradigm', 'occupation','experience']
	id = db.Column('id', db.Integer, primary_key=True)
	firstname = db.Column(db.String(100), nullable=False)
	lastname = db.Column(db.String(100), nullable=False)
	experience = db.Column(db.Text)
	paradigm = db.Column(db.Text)
	occupation = db.Column(db.Text)
	rating = db.Column(db.Integer)


class Post(db.Model):
	__tablename__ = "post"
	id = db.Column(db.Integer, primary_key=True)
	ownerId = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(400), nullable=False)
	content = db.Column(db.Text)
	time = db.Column(db.DateTime, default = datetime.datetime.utcnow)
	rating = db.Column(db.Integer)

	judge_id = db.Column(db.Integer, nullable=False)

wa.whoosh_index(app, Judge)


class newCommentForm(FlaskForm): 
	title = StringField("Title")
	content = StringField("Comment", widget=TextArea())
	rating = IntegerField("Rating")
	submit = SubmitField("Post")
	judgeId = IntegerField("judge Id")

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

class addNewJudgeForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	experience = StringField("Experience", widget=TextArea())
	paradigm = StringField("Paradigm", widget=TextArea())
	occupation = StringField("Occupation", widget=TextArea())
	submit = SubmitField("Add")


@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/post_comment', methods=["POST", "GET"]) 
def post_comment():
	form = newCommentForm()
	if form.validate_on_submit():
		print("successfully validated")
		post = Post(ownerId=current_user.get_id(),
			title=form.title.data,
			content=form.content.data,
			rating=form.rating.data,
			judge_id=form.judgeId.data)
		db.session.add(post)
		db.session.commit()
		return redirect(request.url)
	else:
		return redirect(url_for('index'))

@app.route('/details', methods=["GET"])
def details():
	form = newCommentForm()

	form.judgeId.data = int(request.args.get('judge'))
	
	item = Judge.query.get(request.args.get('judge'))
	comments = Post.query.filter_by(judge_id=item.id).all() 
	usernames=[]
	score = 0
	for comment in comments:
		usernames.append(User.query.get(comment.ownerId).username)
		score += int(comment.rating)

	if(len(comments) != 0):
		score /= len(comments)
		score = int(score)

	else:
		score = "No Scores"

	return render_template('details.html', item=item,
		comments=comments, usernames=usernames, form=form, score=score)

@app.route('/search')
def search():
	results = Judge.query.whoosh_search(request.args.get("jsdata1")).all()
	print(request.args.get('jsdata1'))
	print(results)
	snippets=[]

	for data in results:
		data = data.paradigm
		info = (data[:250] + '..') if len(data) > 250 else data
		snippets.append(info)

	return render_template('search_results.html', results=results, snippets=snippets)

@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/add', methods=['POST', 'GET'])
def add():
	imageUrl = url_for('static', filename="img/display_content/{0}.jpg".format(random.randint(1,9)))

	form = addNewJudgeForm()

	if form.validate_on_submit():
		firstName = form.name.data.split()[0]
		lastName = form.name.data.split()[1]
		judge = Judge(firstname=firstName,
			lastname=lastName,
			experience=form.experience.data,
			paradigm=form.paradigm.data,
			occupation=form.occupation.data)
		db.session.add(judge)
		db.session.commit()

		return redirect(url_for('index'))

	return render_template('add.html', form=form, imageUrl=imageUrl) 

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