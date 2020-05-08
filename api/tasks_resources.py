from flask import jsonify
from flask_restful import abort, Resource
from data.db_session import create_session
from data.models.tasks import Tasks


def abort_if_news_not_found(tasks_id):
    session = create_session()
    tasks = session.query(Tasks).get(tasks_id)
    if not tasks:
        abort(404, message=f"Tasks {tasks_id} not found")


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


class TasksListResources(Resource):
    def get(self):
        session = create_session()
        tasks = session.query(Tasks).all()
        return jsonify({'tasks': [item.to_dict(only=("to_subject", "to_lesson",
                                                     "to_class", "task_date",
                                                     "task_role", "task_file")) for item in tasks]})
