import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Lessons(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True)
    title = sa.Column('title', sa.String, nullable=True)
    to_subject = sa.Column('to_subject', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    to_task = sa.Column('to_task', sa.Integer, sa.ForeignKey("tasks.id"), nullable=True)
    lesson_date = sa.Column('lesson_date', sa.Date, nullable=True)
    author = sa.Column('author', sa.String, sa.ForeignKey("teachers.id"), nullable=True)
    lesson_file = sa.Column('lesson_file', sa.String, nullable=True)

    subjects = sa.orm.relation("Subjects")
    tasks = sa.orm.relation("Tasks")
    teachers = sa.orm.relation("Teachers")
