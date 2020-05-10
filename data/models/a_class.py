import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class AClasses(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'a_classes'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column('title', sa.String, nullable=True, unique=True)
    teacher = sa.Column('teacher', sa.ForeignKey('teachers.id'), nullable=True)
    students_list = sa.Column('students_list', sa.String, nullable=True)
    cur_lessons_list = sa.Column('cur_lessons_list', sa.String, nullable=True)

    teachers = sa.orm.relation("Teachers", foreign_keys=[teacher])
    students = sa.orm.relation("Students")
    lessons = sa.orm.relation("Lessons")