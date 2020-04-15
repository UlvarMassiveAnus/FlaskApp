import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Teachers(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    taught_subject = sa.Column('taught_subject', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    a_class = sa.Column('a_class', sa.ForeignKey("a_classes.id"), nullable=True)
    user_id = sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"))

    lessons = sa.orm.relation("Lessons")
    subjects = sa.orm.relation("Subjects", foreign_keys=[taught_subject])
    a_classes = sa.orm.relation('AClasses', foreign_keys=[a_class])
    users = sa.orm.relation('Users', foreign_keys=[user_id])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return self.hashed_password == password
