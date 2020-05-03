from flask_restful import reqparse


def create_lessons_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True)
    parser.add_argument('to_subject', required=True)
    parser.add_argument('to_task', required=True, type=int)
    parser.add_argument('to_class', required=True, type=int)
    parser.add_argument('lesson_date', required=True)
    parser.add_argument('author', required=True, type=int)
    parser.add_argument('lesson_file', required=True)
    return parser
