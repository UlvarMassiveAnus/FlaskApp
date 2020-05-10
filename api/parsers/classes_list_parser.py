from flask_restful import reqparse


def create_classes_list_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True)
    return parser
