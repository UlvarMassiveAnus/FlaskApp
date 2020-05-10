from data.db_session import create_session
from data.models.a_class import AClasses
from flask_restful import abort, Resource
from flask import jsonify
from api.parsers.classes_list_parser import create_classes_list_parser


def abort_if_news_not_found(class_id):
    session = create_session()
    a_class = session.query(AClasses).get(class_id)
    if not a_class:
        abort(404, message=f"Users {class_id} not found")


class AClassResource(Resource):
    def get(self, class_id):
        abort_if_news_not_found(class_id)
        session = create_session()
        a_class = session.query(AClasses).get(class_id)
        return jsonify({"class": a_class.to_dict(only=("title", "teacher", "cur_lessons_list"))})


class AClassListResource(Resource):
    def get(self):
        session = create_session()
        a_classes = session.query(AClasses).all()
        return jsonify({"classes": [item.to_dict(only=("title", "teacher", "cur_lessons_list")) for item in a_classes]})

    def post(self):
        parser = create_classes_list_parser()
        args = parser.parse_args()
        session = create_session()
        a_class = AClasses(
            title=args['title']
        )
        session.add(a_class)
        session.commit()
        return jsonify({"success": "OK"})