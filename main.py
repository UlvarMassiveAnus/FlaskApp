import os
import datetime
import random
from flask import Flask, render_template, redirect, url_for, request
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_restful import Api
from data.db_session import global_init, create_session
from data.models.lessons import Lessons, lessons_to_students
from data.models.users import Users
from data.models.teachers import Teachers
from data.models.students import Students
from data.models.a_class import AClasses
from data.models.tasks import Tasks
from data.models.lessons_to_students import LessonsToStudents
from forms import LoginForm
from api.lessons_resources import LessonsResources, LessonsListResources
from api.tasks_resources import TasksResources, TasksListResources
from api.users_resources import UsersResources, TeachersListResources, StudentsListResources
from api.classes_resources import AClassResource, AClassListResource

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
    return render_template('home_page.html', current_user=current_user, shadow=find_shadow(current_user))


@app.route('/classes')
def classes():
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Student":
        return redirect("/")

    shadow = find_shadow(current_user)

    session = create_session()
    a_classes = session.query(AClasses).all()
    for cl in a_classes:
        cur_lessons_list = []
        for ls in session.query(Lessons).filter(Lessons.to_class == cl.id).all():
            if ls.lesson_date == datetime.datetime.today().date():
                cur_lessons_list.append(str(ls.id))
        cl.cur_lessons_list = ', '.join(cur_lessons_list)
    session.commit()

    lessons = {}

    session = create_session()
    a_classes = session.query(AClasses).all()
    for cl in a_classes:
        cur_lessons_list = cl.cur_lessons_list.split(", ")
        lessons[cl.title] = [session.query(Lessons).filter(Lessons.id == int(les)).first() for les in cur_lessons_list
                             if les]

    return render_template('classes.html',
                           current_user=current_user,
                           shadow=shadow,
                           a_classes=a_classes,
                           lessons=lessons)


@app.route('/timetable')
def timetable():
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Teacher":
        return redirect("/")

    session = create_session()
    shadow = find_shadow(current_user)

    cl = session.query(AClasses).get(shadow.in_class)
    cur_lessons_list = []

    for ls in session.query(Lessons).filter(Lessons.to_class == cl.id).all():
        if ls.lesson_date == datetime.datetime.today().date():
            cur_lessons_list.append(str(ls.id))

    cl.cur_lessons_list = ', '.join(cur_lessons_list)
    session.commit()

    session = create_session()
    cur_lessons_list = [i for i in cl.cur_lessons_list.split(", ") if i]
    lessons = [session.query(Lessons).filter(Lessons.id == int(les)).first() for les in cur_lessons_list]

    return render_template('timetable.html', current_user=current_user,
                           lessons=lessons, shadow_id=str(shadow.id), none_check=lambda x: x is not None)


@app.route('/lessoncreate/<int:class_id>', methods=['GET', 'POST'])
def lessoncreate(class_id):
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Student":
        return redirect("/")

    if request.method == 'GET':
        return render_template('lessoncreate.html', url_for=url_for, class_id=class_id, message='')
    elif request.method == 'POST':
        files_data = request.files.to_dict()
        files_paths = {}

        text_data = request.form.to_dict()
        file = []

        if not request.form['date']:
            return render_template('lessoncreate.html', url_for=url_for,
                                   class_id=request.form['class_id'], message="Обозначьте дату")
        elif len(text_data.keys()) <= 4:
            return render_template('lessoncreate.html', url_for=url_for,
                                   class_id=request.form['class_id'], message="Добавьте хотя бы один параграф")

        shadow = find_shadow(current_user)

        for input_name in files_data.keys():
            file_prefix = int(datetime.datetime.today().timestamp())
            filepath = os.path.join("static", "img", str(file_prefix) + "_" + files_data[input_name].filename)
            files_paths[input_name] = str(file_prefix) + "_" + files_data[input_name].filename
            files_data[input_name].save(dst=filepath)

        for key in [i for i in files_data.keys() if i[-1].isdigit()] + [i for i in text_data.keys() if i[-1].isdigit()]:
            file.insert(int(key[-1]) - 1, key)

        file_prefix = int(datetime.datetime.today().timestamp())
        with open(f"lessons/{file_prefix}_lesson.txt", "w") as f:
            f.write(f"{text_data['lsnm1']}\n")
            for key in file[1:]:
                try:
                    f.write(text_data[key].replace("\n", ""))
                except Exception:
                    f.write(f"\n[{files_paths[key]}]\n")

        session = create_session()
        lesson = Lessons(title=request.form['lsnm1'],
                         to_subject=shadow.taught_subject,
                         to_class=request.form['class_id'],
                         lesson_date=datetime.date(*[int(item) for item in request.form['date'].split('-')]),
                         author=shadow.id,
                         role=request.form['role'],
                         lesson_file=f"{file_prefix}_lesson.txt")

        session.add(lesson)
        session.commit()
        return redirect(f'/testcreate/{lesson.id}')


@app.route('/testcreate/<int:lesson_id>', methods=['GET', 'POST'])
def testcreate(lesson_id):
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Student":
        return redirect("/")

    if request.method == 'GET':
        return render_template('testcreate.html', url_for=url_for, lesson_id=lesson_id, message="")
    elif request.method == 'POST':
        data = request.form.to_dict()

        print(data)

        if len(data) < 21:
            return render_template("testcreate.html", url_for=url_for,
                                   lesson_id=request.form['lesson_id'],
                                   message="Тест должен содержать минимум 4 вопроса")

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
                     task_date=datetime.datetime.today().date(),
                     task_file=f'{file_prefix}_task.txt')
        session = create_session()
        session.add(task)
        session.commit()

        lesson = session.query(Lessons).get(lesson_id)
        lesson.to_task = task.id
        session.commit()
        return redirect('/')


@app.route('/readlesson/<int:lesson_id>')
def readlesson(lesson_id):
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Teacher":
        return redirect("/")

    session = create_session()
    lesson = session.query(Lessons).get(lesson_id)
    with open(f"lessons/{lesson.lesson_file}") as f:
        data = f.readlines()
        for line in range(len(data)):
            data[line] = data[line].strip("\n")

    return render_template('readlesson.html', data=data,
                           current_user=current_user,
                           url_for=url_for,
                           to_task=lesson.to_task)


@app.route('/readtest/<int:task_id>', methods=['GET', 'POST'])
def readtest(task_id):
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Teacher":
        return redirect("/")

    if request.method == 'GET':
        session = create_session()
        task = session.query(Tasks).get(task_id)
        with open(f"tasks/{task.task_file}") as f:
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
                               task_id=task_id)
    elif request.method == 'POST':
        mark = 0
        for i, r in enumerate(request.form["right_answers"]):
            if request.form[str(i + 1)] == r:
                mark += 1
        mark = int((mark / len(request.form["right_answers"])) * 100)

        if mark >= 75:
            session = create_session()
            task = session.query(Tasks).get(request.form["task_id"])
            lesson = session.query(Lessons).get(task.to_lesson)
            completed_by = lesson.completed_by
            if completed_by is None or not completed_by:
                completed_by = []
            else:
                completed_by = completed_by.split(", ")
            shadow = find_shadow(current_user)
            if str(shadow.id) not in completed_by:
                completed_by.append(str(shadow.id))
            lesson.completed_by = ", ".join(completed_by)

            new_conn = LessonsToStudents(lessons_id=lesson.id, students_id=shadow.id, mark=mark)
            session.add(new_conn)
            session.commit()
            added_conn = session.query(LessonsToStudents).get(1)
            print(added_conn.students, added_conn.lessons)
        return render_template('result.html', mark=mark)


@app.route('/students')
def students():
    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.role == "Student":
        return redirect("/")

    shadow = find_shadow(current_user)
    session = create_session()
    sts = [st for st in session.query(Students).filter(Students.in_class == shadow.a_class)]
    return render_template('students.html', students=sts)


@app.route('/marks')
def marks():
    if not current_user.is_authenticated:
        return redirect('/login')
    if current_user.role == "Teacher":
        return redirect("/")

    shadow = find_shadow(current_user)
    session = create_session()
    cmpl = [ls for ls in session.query(Lessons).all() if
            ls.completed_by is not None and str(shadow.id) in ls.completed_by.split(', ')]
    return render_template('marks.html', lessons=cmpl)


@app.route('/journal')
def journal():
    if not current_user.is_authenticated:
        return redirect('/login')
    if current_user.role == 'Student':
        return redirect('/')

    shadow = find_shadow(current_user)
    session = create_session()
    lessons = [[ls.title, ls.role, ls.lesson_date, ls.to_class, [(session.query(Users).get(session.query(Students).get(conn.students_id).user_id), conn.mark) for conn in session.query(LessonsToStudents).filter(LessonsToStudents.lessons_id == ls.id)]] for ls in session.query(Lessons).filter(Lessons.to_class == shadow.a_class)]
    return render_template('journal.html', lessons=lessons)


if __name__ == '__main__':
    global_init("db/project.sqlite")
    api.add_resource(LessonsResources, '/api/v1/lessons/<int:lessons_id>')
    api.add_resource(LessonsListResources, "/api/v1/lessons")
    api.add_resource(TasksResources, '/api/v1/tasks/<int:tasks_id>')
    api.add_resource(TasksListResources, '/api/v1/tasks')
    api.add_resource(UsersResources, '/api/v1/users/<int:users_id>')
    api.add_resource(TeachersListResources, '/api/v1/teachers')
    api.add_resource(StudentsListResources, '/api/v1/students')
    api.add_resource(AClassResource, '/api/v1/classes/<int:class_id>')
    api.add_resource(AClassListResource, '/api/v1/classes')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
