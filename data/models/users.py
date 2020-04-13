import sqlalchemy as sa
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    surname = sa.Column('surname', sa.String, nullable=True)
    name = sa.Column('name', sa.String, nullable=True)
    lessons_list = sa.Column('lessons_list', sa.String, nullable=True)
    birth_date = sa.Column('birth_date', sa.Date, nullable=True)
    in_class = sa.Column('class', sa.Integer, nullable=True)
    about = sa.Column('about', sa.String, nullable=True)
    email = sa.Column('email', sa.String, nullable=True, unique=True)
    hashed_password = sa.Column('password', sa.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return self.hashed_password == password
