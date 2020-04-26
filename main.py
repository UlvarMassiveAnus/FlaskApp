import os
import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from data.db_session import global_init, create_session
from data.models.lessons import Lessons
from data.models.users import Users
from data.models.teachers import Teachers
from data.models.students import Students
from data.models.a_class import AClasses
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '0e294ca639af91b8aaefcdd6ccdbd9b1'

login_manager = LoginManager()
login_manager.init_app(app)


def find_shadow(user):
    session = create_session()
    if user.role == 'Student':
        return session.query(Students).filter(Students.user_id == user.id).first()
    elif user.role == 'Teacher':
        return session.query(Teachers).filter(Teachers.user_id == user.id).first()


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
    session = create_session()
    shadow = find_shadow(current_user)
    if current_user.role == "Teacher":
        a_classes = session.query(AClasses).all()
        lessons = {}
        for cl in a_classes:
            cur_lessons_list = cl.cur_lessons_list.split(", ")
            lessons[cl.title] = [session.query(Lessons).filter(Lessons.id == int(les)).first() for les in
                                 cur_lessons_list]
    else:
        return redirect("/")
    return render_template('classes.html',
                           current_user=current_user,
                           shadow=shadow,
                           a_classes=a_classes,
                           lessons=lessons)


@app.route('/courses')
def courses():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('courses.html', current_current_user=current_user)


@app.route('/timetable')
def timetable():
    if not current_user.is_authenticated:
        return redirect("/login")
    session = create_session()
    shadow = find_shadow(current_user)
    if current_user.role == "Student":
        cl = session.query(AClasses).get(shadow.in_class)
        cur_lessons_list = cl.cur_lessons_list.split(", ")
        lessons = [session.query(Lessons).get(int(les)) for les in cur_lessons_list]
    else:
        return redirect("/")
    return render_template('timetable.html', current_user=current_user, lessons=lessons)


@app.route('/settings')
def settings():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('settings.html', current_user=current_user)


@app.route('/lessoncreate', methods=['GET', 'POST'])
def lessoncreate():
    if request.method == 'GET':
        return render_template('lessoncreate.html', url_for=url_for)
    elif request.method == 'POST':
        os.mkdir(path=os.path.join("lessons", "id_lesson"))
        files_data = request.files.to_dict()
        text_data = request.form.to_dict()
        file = []
        for input_name in files_data.keys():
            files_data[input_name].save(dst=os.path.join("lessons", "id_lesson",
                                                         str(current_user.id) + "_" + files_data[input_name].filename))
        for key in [i for i in files_data.keys()] + [i for i in text_data.keys()]:
            file.insert(int(key[-1]) - 1, key)
        with open("lessons/id_lesson/id_lesson.txt", "w") as f:
            for key in file:
                try:
                    f.write(text_data[key].replace("\n", "") + "\n")
                except Exception:
                    f.write(f"[{files_data[key].filename}]\n")
        return redirect('/')


@app.route('/testcreate', methods=['GET', 'POST'])
def testcreate():
    if request.method == 'GET':
        return render_template('testcreate.html', url_for=url_for)
    elif request.method == 'POST':
        os.mkdir(path=os.path.join("tasks", "id_task"))
        data = request.form.to_dict()
        file = []
        for key in data:
            if "qst" in key:
                file.insert(int(key[-1]) - 1, (key,
                                               f"wrn1-{key[-1]}",
                                               f"wrn2-{key[-1]}",
                                               f"wrn3-{key[-1]}",
                                               f"rgh4-{key[-1]}"))
        print(data, file)
        with open("tasks/id_task/id_task.txt", "w") as f:
            for key in file:
                f.write(data[key[0]] + "\n")
                f.write(f"[1{data[key[1]]}]" + "\n")
                f.write(f"[2{data[key[2]]}]" + "\n")
                f.write(f"[3{data[key[3]]}]" + "\n")
                f.write(f"[4{data[key[4]]}]" + "\n")
                f.write("|NewQuestion|\n")
        return redirect('/')


if __name__ == '__main__':
    global_init("db/project.sqlite")
    app.run()
