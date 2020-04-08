import sqlalchemy as sa
from data.db_session import SqlAlchemyBase


class Subjects(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True)
    subjects = sa.Column('subject_name', sa.Integer, nullable=True)

    teachers = sa.orm.relation("Teachers")
    tasks = sa.orm.relation("Tasks")
    lessons = sa.orm.relation("Lessons", back_populates='subjects')