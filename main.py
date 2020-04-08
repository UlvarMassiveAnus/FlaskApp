from flask import Flask, render_template
from flask_login import current_user
from data.db_session import global_init, create_session
from data.models.lessons import Lessons

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home_page.html', current_user=current_user)


@app.route('/classes')
def classes():
    return render_template('', current_user=current_user)


@app.route('/courses')
def courses():
    return render_template('', current_user=current_user)


@app.route('/timetable')
def timetable():
    lessons = [lesson for lesson in current_user.lessons]
    return render_template('', current_user=current_user, lessons=lessons)


@app.route('/settings')
def settings():
    return render_template('', current_user=current_user)


if __name__ == '__main__':
    global_init("db/project.sqlite")
    app.run()
