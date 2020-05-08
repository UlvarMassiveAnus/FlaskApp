from flask import jsonify
from flask_restful import abort, Resource
from data.db_session import create_session
from data.models.lessons import Lessons


def abort_if_news_not_found(lessons_id):
    session = create_session()
    lessons = session.query(Lessons).get(lessons_id)
    if not lessons:
        abort(404, message=f"Lessons {lessons_id} not found")


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
        task = lesson.tasks
        if task is not None:
            task.to_lesson = None
        session.commit()
        session.delete(lesson)
        session.commit()
        session.delete(task)
        session.commit()
        return jsonify({'success': 'OK'})


class LessonsListResources(Resource):
    def get(self):
        session = create_session()
        lessons = session.query(Lessons).all()
        return jsonify({'lessons': [item.to_dict(only=("title", "to_subject",
                                                       "to_task", "to_class",
                                                       "lesson_date", "author",
                                                       "lesson_file")) for item in lessons]})
