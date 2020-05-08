from flask_restful import reqparse


def create_users_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('surname', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('birth_date', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)
    parser.add_argument('role', required=True)
    return parser


def teacher_parser():
    parser = create_users_list_parser()
    parser.add_argument('taught_subject', required=True, type=int)
    parser.add_argument('a_class', required=True, type=int)
    return parser


def student_parser():
    parser = create_users_list_parser()
    parser.add_argument('in_class', required=True, type=int)
    return parser
