from flask import Flask, render_template, redirect, request, url_for,flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, length, Email, EqualTo,ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), length(min=3, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This Username is Already exist in Database.Try another")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This Email is Already exist in Database.Try another")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])

"""
import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
"""



app = Flask(__name__)

# 192.168.43.187 or localhost
app.config['SECRET_KEY'] = '8242e3346ba731277bd78d1e9c4bf76a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:159159@localhost/surveillance_robot'

db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(90), nullable=False)

    def __repr__(self):
        return f"USer({self.username},{self.email})"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        flash("Authorization Access Created Successfully")
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                username = current_user.username
                flash("You Access has been granted ")
                return redirect(url_for('dashboard'))
            else:
                flash('Please Enter Correct Password')
                return render_template('login.html', title='Login', form=form)

        else:
            flash("Invalid Credentials.User email and Password are Incorrect")
            return render_template('login.html', title='Login', form=form)
    else:
        return render_template('login.html', title='Login', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/<action>")
@login_required
def robot(action):
    r_status = "off"
    if action == 'reverse':
        r_status = 'REVERESE'
        reverse()
    elif(action == 'fwd'):
        r_status = 'FORWARD'
        forward()
    elif(action == 'left'):
        r_status = "LEFT"
        pivot_left()
    elif(action == 'right'):
        r_status = "RIGHT"
        pivot_right()
    elif(action == 'stop'):
        r_status = "STOP"
        turn_off()


    data = {
        'r_status': r_status,
    }

    return render_template("dashboard.html", data=data)


@app.route("/dashboard/cam/stream")
@login_required
def stream(action):
    return render_template("cam.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def forward():
    gpio.output(13, False)
    gpio.output(15, True)
    gpio.output(7, False)
    gpio.output(11, True)


def reverse():
    gpio.output(13, True)
    gpio.output(15, False)
    gpio.output(7, True)
    gpio.output(11, False)


def pivot_right():
    gpio.output(13, False)
    gpio.output(15, True)
    gpio.output(7, True)
    gpio.output(11, False)


def pivot_left():
    gpio.output(13, True)
    gpio.output(15, False)
    gpio.output(7, False)
    gpio.output(11, True)



def turn_off():
    gpio.output(13, True)
    gpio.output(15, True)
    gpio.output(7, True)
    gpio.output(11, True)

"""
def turn_left():

    gpio.output(13, True)
    gpio.output(15, True)
    gpio.output(7, False)
    gpio.output(11, True)



def turn_right():
    gpio.output(13, False)
    gpio.output(15, True)
    gpio.output(7, True)
    gpio.output(11, True)
"""

if __name__ == "__main__":
    app.run()
