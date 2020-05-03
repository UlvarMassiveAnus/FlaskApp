from flask import jsonify
from .parsers.lessons_list_resources_parser import create_lessons_list_parser
from flask_restful import abort, Resource
from data.db_session import create_session
from data.models.lessons import Lessons
import datetime


def abort_if_news_not_found(lessons_id):
    session = create_session()
    news = session.query(Lessons).get(lessons_id)
    if not news:
        abort(404, message=f"News {lessons_id} not found")


class LessonsResources(Resource):
    def get(self, lessons_id):
        abort_if_news_not_found(lessons_id)
        session = create_session()
        lesson = session.query(Lessons).get(lessons_id)
        return jsonify(
            {
                'lessons': lesson.to_dict(only=("title", "to_subject",
                                                "to_task", "to_class",
                                                "lesson_date", "author",
                                                "lesson_file"))
            }
        )

    def delete(self, lessons_id):
        abort_if_news_not_found(lessons_id)
        session = create_session()
        lesson = session.query(Lessons).get(lessons_id)
        session.delete(lesson)
        session.commit()
        return jsonify({'success': 'OK'})


class LessonsListResources(Resource):
    def get(self):
        session = create_session()
        lessons = session.query(Lessons).all()
        return jsonify({'news': [item.to_dict(only=("title", "to_subject",
                                                    "to_task", "to_class",
                                                    "lesson_date", "author",
                                                    "lesson_file")) for item in lessons]})

    def post(self):
        parser = create_lessons_list_parser()
        args = parser.parse_args()
        session = create_session()
        lesson = Lessons(
            title=args['title'],
            to_subject=args['to_subject'],
            to_task=args['to_task'],
            to_class=args['to_class'],
            lesson_date=datetime.date(*[int(item) for item in args['lesson_date'].split('-')]),
            author=args['author'],
            lesson_file=args['lesson_file']
        )
        session.add(lesson)
        session.commit()
        return jsonify({'success': 'OK'})
