import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

lessons_to_students = sa.Table('lessons_to_students',
                               SqlAlchemyBase.metadata,
                               sa.Column('lessons_id', sa.Integer, sa.ForeignKey('lessons.id')),
                               sa.Column('students_id', sa.Integer, sa.ForeignKey('students.id')),
                               sa.Column('mark', sa.Integer))


class Lessons(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lessons'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    title = sa.Column('title', sa.String, nullable=True)
    to_subject = sa.Column('to_subject', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    to_task = sa.Column('to_task', sa.Integer, sa.ForeignKey("tasks.id"), nullable=True)
    to_class = sa.Column('to_class', sa.Integer, sa.ForeignKey("a_classes.id"), nullable=True)
    role = sa.Column('role', sa.String, nullable=True)
    lesson_date = sa.Column('lesson_date', sa.Date, nullable=True)
    author = sa.Column('author', sa.String, sa.ForeignKey("teachers.id"), nullable=True)
    completed_by = sa.Column('completed_by', sa.String, nullable=True)
    lesson_file = sa.Column('lesson_file', sa.String, nullable=True)

    subjects = sa.orm.relation("Subjects", foreign_keys=[to_subject])
    tasks = sa.orm.relation("Tasks", foreign_keys=[to_task])
    teachers = sa.orm.relation("Teachers", foreign_keys=[author])
    a_classes = sa.orm.relation("AClasses", foreign_keys=[to_class])
    lessons_to_students = sa.orm.relation("LessonsToStudents")
