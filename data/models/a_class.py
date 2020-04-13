import sqlalchemy as sa
from data.db_session import SqlAlchemyBase


class AClasses(SqlAlchemyBase):
    __tablename__ = 'a_classes'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column('title', sa.String, nullable=True)
    teacher = sa.Column('teacher', sa.ForeignKey('teachers.id'), nullable=True)
    users_list = sa.Column('users_list', sa.String, nullable=True)
    cur_lesson = sa.Column('cur_lesson', sa.ForeignKey('lessons.id'), nullable=True)

    teachers = sa.orm.relation("Teachers", foreign_keys=[teacher])
    lessons = sa.orm.relation("Lessons", foreign_keys=[cur_lesson])