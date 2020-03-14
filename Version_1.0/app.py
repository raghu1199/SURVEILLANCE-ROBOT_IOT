from flask import Flask, render_template, redirect, request, url_for
from forms import RegistrationForm, LoginForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, logout_user, current_user, login_user
#import RPi.GPIO as gpio
import time

app = Flask(__name__)

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
        return "<h1>" + form.username.data + " " + form.email.data + " " + form.password.data + "</h1>"
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
                return redirect(url_for('dashboard'))
            else:
                return "<h1>Invalid Credentials</h1>"
    return render_template('login.html', title='Login', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    gpio.cleanup()


def forward():
    init()
    gpio.output(13, False)
    gpio.output(15, True)
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.cleanup()


def reverse():
    init()
    gpio.output(13, True)
    gpio.output(15, False)
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.cleanup()


def turn_left():
    init()
    gpio.output(13, True)
    gpio.output(15, True)
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.cleanup()


def turn_right():
    init()
    gpio.output(13, False)
    gpio.output(15, True)
    gpio.output(7, True)
    gpio.output(11, True)
    gpio.cleanup()


def pivot_right():
    init()
    gpio.output(13, False)
    gpio.output(15, True)
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.cleanup()


def turn_off():
    init()
    gpio.output(13, True)
    gpio.output(15, True)
    gpio.output(7, True)
    gpio.output(11, True)
    gpio.cleanup()

"""  r_status = "off"
    if action == 'down_side':
        r_status = 'REVRESE'
        reverse()
    elif (action == 'up_side'):
        r_status = 'FORWARD'
        forward()
    elif (action == 'left_side'):
        r_status = "LEFT"
        turn_left()
    elif (action == 'right_side'):
        r_status = "RIGHT"
        turn_right()
    elif (action == 'stop'):
        r_status = "STOP"
        turn_off()"""


if __name__ == "__main__":
    app.run()
