import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    surname = sa.Column('surname', sa.String, nullable=True)
    name = sa.Column('name', sa.String, nullable=True)
    birth_date = sa.Column('birth_date', sa.Date, nullable=True)
    role = sa.Column('role', sa.String, nullable=True)
    email = sa.Column('email', sa.String, nullable=True, unique=True)
    hashed_password = sa.Column('hashed_password', sa.String, nullable=True)

    teachers = sa.orm.relation("Teachers")
    students = sa.orm.relation("Students")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return self.hashed_password == password
