import sqlalchemy as sa
from data.db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True)
    to_subject = sa.Column('to_sublect', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    to_lesson = sa.Column('to_lesson', sa.Integer, sa.ForeignKey("lessons.id"), nullable=True)
    mark = sa.Column('mark', sa.Integer, nullable=True)
    task_date = sa.Column('task_date', sa.Date, nullable=True)
    task_role = sa.Column('task_role', sa.String, nullable=True)
    task_file = sa.Column('task_file', sa.Integer, nullable=True)

    lessons = sa.orm.relation("Lessons", back_populates='tasks')
    subjects = sa.orm.relation("Subjects", back_populates='tasks')