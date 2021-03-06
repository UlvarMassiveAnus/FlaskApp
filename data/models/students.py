import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Students(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    lessons_list = sa.Column('lessons_list', sa.String, nullable=True)
    in_class = sa.Column('class', sa.Integer, sa.ForeignKey("a_classes.id"), nullable=True)
    user_id = sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"))

    users = sa.orm.relation('Users', foreign_keys=[user_id])
    a_classes = sa.orm.relation('AClasses', foreign_keys=[in_class])
    lessons_to_students = sa.orm.relation("LessonsToStudents")

