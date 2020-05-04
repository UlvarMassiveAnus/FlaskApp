import os
import datetime
import random
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_restful import Api
from data.db_session import global_init, create_session
from data.models.lessons import Lessons
from data.models.users import Users
from data.models.teachers import Teachers
from data.models.students import Students
from data.models.a_class import AClasses
from data.models.subjects import Subjects
from data.models.tasks import Tasks
from forms import LoginForm
from api.lessons_resources import LessonsResources, LessonsListResources
from api.tasks_resources import TasksResources, TasksListResources

app = Flask(__name__)
app.config['SECRET_KEY'] = '0e294ca639af91b8aaefcdd6ccdbd9b1'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


def find_shadow(user):
    session = create_session()
    if user.role == 'Student':
        return session.query(Students).filter(Students.user_id == user.id).first()
    elif user.role == 'Teacher':
        return session.query(Teachers).filter(Teachers.user_id == user.id).first()


def randomize_questions(n):
    reference = [1, 2, 3, 4]
    result = []
    for i in range(n):
        random.shuffle(reference)
        result += reference
    return result


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
        files_data = request.files.to_dict()
        text_data = request.form.to_dict()
        file = []
        shadow = find_shadow(current_user)
        session = create_session()
        for input_name in files_data.keys():
            filepath = os.path.join("static", "img", str(int(datetime.datetime.today().timestamp())) + "_" + files_data[
                input_name].filename)
            files_data[input_name].save(dst=filepath)
        for key in [i for i in files_data.keys()] + [i for i in text_data.keys()]:
            file.insert(int(key[-1]) - 1, key)
        file_prefix = int(datetime.datetime.today().timestamp())
        with open(f"lessons/{file_prefix}_lesson.txt", "w") as f:
            for key in file:
                try:
                    f.write(text_data[key].replace("\n", ""))
                except Exception:
                    f.write(f"\n[{str(current_user.id) + '_' + files_data[key].filename}]\n")
        lesson = Lessons(title="TITLE",
                         to_subject=shadow.taught_subject,
                         to_class=shadow.a_class,
                         lesson_date=datetime.date(2020, 11, 1),
                         author=shadow.id,
                         lesson_file=f"{file_prefix}_lesson.txt")
        session.add(lesson)
        session.commit()
        return redirect(f'/testcreate/{lesson.id}')


@app.route('/testcreate/<int:lesson_id>', methods=['GET', 'POST'])
def testcreate(lesson_id):
    if request.method == 'GET':
        return render_template('testcreate.html', url_for=url_for, lesson_id=lesson_id)
    elif request.method == 'POST':
        data = request.form.to_dict()
        file = []
        shadow = find_shadow(current_user)
        lesson_id = request.form['lesson_id']
        for key in data:
            if "qst" in key:
                file.insert(int(key[-1]) - 1, (key,
                                               f"wrn1-{key[-1]}",
                                               f"wrn2-{key[-1]}",
                                               f"wrn3-{key[-1]}",
                                               f"rgh4-{key[-1]}"))
        file_prefix = int(datetime.datetime.today().timestamp())
        with open(f"tasks/{file_prefix}_task.txt", "w") as f:
            for key in file:
                f.write(data[key[0]] + "\n")
                f.write(f"[{data[key[1]]}]" + "\n")
                f.write(f"[{data[key[2]]}]" + "\n")
                f.write(f"[{data[key[3]]}]" + "\n")
                f.write(f"[{data[key[4]]}]" + "\n")
                f.write("|NewQuestion|\n")
        task = Tasks(to_subject=shadow.taught_subject,
                     to_lesson=lesson_id,
                     task_date=datetime.date(2020, 11, 1),
                     task_role="TEST",
                     task_file=f'{file_prefix}_task.txt')
        session = create_session()
        lesson = session.query(Lessons).get(lesson_id)
        lesson.to_task = task.id
        session.add(task)
        session.commit()
        return redirect('/')


@app.route('/readlesson')
def readlesson():
    if not current_user.is_authenticated:
        return redirect('/login')
    with open("lessons/id_lesson.txt") as f:
        data = f.readlines()
        for line in range(len(data)):
            data[line] = data[line].strip("\n")
    return render_template('readlesson.html', data=data,
                           current_user=current_user,
                           url_for=url_for)


@app.route('/readtest', methods=['GET', 'POST'])
def readtest():
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        with open("tasks/id_task.txt") as f:
            data = f.readlines()
            for line in range(len(data)):
                data[line] = data[line].strip("\n")
        qst_list = []
        file = []
        for line in data:
            line = line.strip('\n')
            if line == "|NewQuestion|":
                file.append(qst_list)
                qst_list = []
            else:
                qst_list.append(line.strip("[").strip("]"))
        rand = randomize_questions(len(file))
        return render_template('readtest.html', data=file,
                               current_user=current_user, rand=rand,
                               right_answers="".join([str(i % 4 + 1) for i in range(len(rand)) if rand[i] == 4]),
                               task_id="test_value")
    elif request.method == 'POST':
        mark = 0
        for i, r in enumerate(request.form["right_answers"]):
            if request.form[str(i + 1)] == r:
                mark += 1
        return render_template('result.html', mark=int((mark / len(request.form["right_answers"])) * 100))


if __name__ == '__main__':
    global_init("db/project.sqlite")
    api.add_resource(LessonsResources, '/api/v1/lessons/<int:lessons_id>')
    api.add_resource(LessonsListResources, "/api/v1/lessons")
    api.add_resource(TasksResources, '/api/v1/tasks/<int:tasks_id>')
    api.add_resource(TasksListResources, '/api/v1/tasks')
    app.run()
