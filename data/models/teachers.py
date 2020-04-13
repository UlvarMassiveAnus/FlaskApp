import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class Teachers(SqlAlchemyBase, UserMixin):
    __tablename__ = 'teachers'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    surname = sa.Column('surname', sa.String, nullable=True)
    name = sa.Column('name', sa.String, nullable=True)
    taught_subject = sa.Column('taught_subject', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    a_class = sa.Column('a_class', sa.ForeignKey("a_classes.id"), nullable=True)
    birth_date = sa.Column('birth_date', sa.Date, nullable=True)
    about = sa.Column('about', sa.String, nullable=True)
    email = sa.Column('email', sa.String, nullable=True, unique=True)
    hashed_password = sa.Column('hashed_password', sa.String, nullable=True)

    lessons = sa.orm.relation("Lessons")
    subjects = sa.orm.relation("Subjects", foreign_keys=[taught_subject])
    a_classes = sa.orm.relation('AClasses', foreign_keys=[a_class])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return self.hashed_password == password