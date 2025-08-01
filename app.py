from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Notification, ExamResult, Timetable
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    notifications = Notification.get_all()
    results = ExamResult.get_by_user(current_user.id)
    timetable = Timetable.get_by_user(current_user.id)
    return render_template('dashboard.html', notifications=notifications, results=results, timetable=timetable)

if __name__ == '__main__':
    app.run(debug=True)
