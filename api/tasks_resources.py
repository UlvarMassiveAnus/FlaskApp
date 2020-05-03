from flask import jsonify
from .parsers.tasks_list_resources_parser import create_tasks_list_parser
from flask_restful import abort, Resource
from data.db_session import create_session
from data.models.tasks import Tasks
import datetime


def abort_if_news_not_found(tasks_id):
    session = create_session()
    news = session.query(Tasks).get(tasks_id)
    if not news:
        abort(404, message=f"News {tasks_id} not found")


class TasksResources(Resource):
    def get(self, tasks_id):
        abort_if_news_not_found(tasks_id)
        session = create_session()
        task = session.query(Tasks).get(tasks_id)
        return jsonify(
            {
                'tasks': task.to_dict(only=("to_subject", "to_lesson",
                                            "to_class", "task_date",
                                            "task_role", "task_file"))
            }
        )

    def delete(self, tasks_id):
        abort_if_news_not_found(tasks_id)
        session = create_session()
        task = session.query(Tasks).get(tasks_id)
        session.delete(task)
        session.commit()
        return jsonify({'success': 'OK'})


class TasksListResources(Resource):
    def get(self):
        session = create_session()
        tasks = session.query(Tasks).all()
        return jsonify({'news': [item.to_dict(only=("to_subject", "to_lesson",
                                                    "to_class", "task_date",
                                                    "task_role", "task_file")) for item in tasks]})

    def post(self):
        parser = create_tasks_list_parser()
        args = parser.parse_args()
        session = create_session()
        task = Tasks(
            to_subject=args['to_subject'],
            to_lesson=args['to_lesson'],
            to_class=args['to_class'],
            task_date=datetime.date(*[int(item) for item in args['task_date'].split('-')]),
            task_role=args['task_role'],
            task_file=args['task_file']
        )
        session.add(task)
        session.commit()
        return jsonify({'success': 'OK'})
