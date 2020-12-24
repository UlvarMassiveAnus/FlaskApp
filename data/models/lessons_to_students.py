import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class LessonsToStudents(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lessons_to_students'
    __table_args__ = {'extend_existing': True}

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    lessons_id = sa.Column('lessons_id', sa.Integer, sa.ForeignKey('lessons.id'))
    students_id = sa.Column('students_id', sa.Integer, sa.ForeignKey('students.id'))
    mark = sa.Column('mark', sa.Integer)

    lessons = sa.orm.relation("Lessons", foreign_keys=[lessons_id])
    students = sa.orm.relation("Students", foreign_keys=[students_id])
