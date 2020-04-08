import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True)
    to_subject = sa.Column('to_sublect', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    to_user = sa.Column('to_user', sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    mark = sa.Column('mark', sa.Integer, nullable=True)
    task_date = sa.Column('task_date', sa.Date, nullable=True)
    task_role = sa.Column('task_role', sa.String, nullable=True)
    task_file = sa.Column('task_file', sa.Integer, nullable=True)

    users = sa.orm.relation("Users")
    lessons = sa.orm.relation("Lessons", back_populates='tasks')
    subjects = sa.orm.relation("Subjects", back_populates='tasks')