from flask_restful import reqparse


def create_tasks_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('to_subject', required=True)
    parser.add_argument('to_lesson', required=True, type=int)
    parser.add_argument('to_class', required=True, type=int)
    parser.add_argument('task_date', required=True)
    parser.add_argument('task_role', required=True, type=int)
    parser.add_argument('task_file', required=True)
    parser.add_argument('key', required=True)
    return parser
