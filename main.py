from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from data.db_session import global_init, create_session
from data.models.lessons import Lessons
from data.models.users import Users
from data.models.teachers import Teachers
from data.models.students import Students
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '0e294ca639af91b8aaefcdd6ccdbd9b1'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(Users).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, url_for=url_for)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('home_page.html', current_user=current_user)


@app.route('/classes')
def classes():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('classes.html', current_user=current_user)


@app.route('/courses')
def courses():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('courses.html', current_current_user=current_user)


@app.route('/timetable')
def timetable():
    # if not current_user.is_authenticated:
    #    return redirect("/login")
    session = create_session()
    lessons = [session.query(Lessons).get(int(lesson)) for lesson in session.query(Users).first().lessons]
    return render_template('timetable.html', current_user=current_user, lessons=lessons)


@app.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('settings.html', current_user=current_user)


if __name__ == '__main__':
    global_init("db/project.sqlite")
    app.run()
