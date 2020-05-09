from api.parsers.users_list_parser import teacher_parser, student_parser
from flask import jsonify
from flask_restful import abort, Resource
from data.db_session import create_session
from data.models.users import Users
from data.models.teachers import Teachers
from data.models.students import Students
from data.models.a_class import AClasses
import datetime


def abort_if_news_not_found(users_id):
    session = create_session()
    users = session.query(Users).get(users_id)
    if not users:
        abort(404, message=f"Users {users_id} not found")


class UsersResources(Resource):
    def get(self, users_id):
        abort_if_news_not_found(users_id)
        session = create_session()
        user = session.query(Users).get(users_id)
        return jsonify(
            {
                'users': user.to_dict(only=("surname", "name", "birth_date", "role"))
            }
        )

    def delete(self, users_id):
        abort_if_news_not_found(users_id)
        session = create_session()
        user = session.query(Users).get(users_id)
        if user.role == "Teacher":
            shadow = session.query(Teachers).filter(Teachers.user_id == user.id).first()
            a_class = session.query(AClasses).get(shadow.a_class)
            a_class.teacher = 1
            session.commit()
            session.delete(shadow)
            session.commit()
            session.delete(user)
            session.commit()
        elif user.role == "Student":
            shadow = session.query(Students).filter(Students.user_id == user.id).first()
            session.delete(shadow)
            session.commit()
            session.delete(user)
            session.commit()
        return jsonify({'success': 'OK'})


class TeachersListResources(Resource):
    def get(self):
        session = create_session()
        teachers = session.query(Users).filter(Users.role == "Teacher")
        return jsonify({'teachers': [item.to_dict(only=("surname", "name", "birth_date")) for item in teachers]})

    def post(self):
        session = create_session()
        parser = teacher_parser()
        args = parser.parse_args()
        user = Users(
            surname=args['surname'],
            name=args['name'],
            birth_date=datetime.date(*[int(item) for item in args['birth_date'].split('-')]),
            role=args['role'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        user = session.query(Users).filter(Users.email == args['email']).first()
        teacher = Teachers(
            taught_subject=args['taught_subject'],
            a_class=args['a_class'],
            user_id=user.id
        )
        session.add(teacher)
        session.commit()
        teacher = session.query(Teachers).filter(Teachers.user_id == user.id).first()
        a_class = session.query(AClasses).get(teacher.a_class)
        a_class.teacher = teacher.id
        session.commit()
        return jsonify({'success': 'OK'})


class StudentsListResources(Resource):
    def get(self):
        session = create_session()
        students = session.query(Users).filter(Users.role == "Student")
        return jsonify({'students': [item.to_dict(only=("surname", "name", "birth_date")) for item in students]})

    def post(self):
        session = create_session()
        parser = student_parser()
        args = parser.parse_args()
        user = Users(
            surname=args['surname'],
            name=args['name'],
            birth_date=datetime.date(*[int(item) for item in args['birth_date'].split('-')]),
            role=args['role'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        user = session.query(Users).filter(Users.email == args['email']).first()
        student = Students(
            in_class=args['in_class'],
            user_id=user.id
        )
        session.add(student)
        session.commit()
        return jsonify({"success": 'OK'})
