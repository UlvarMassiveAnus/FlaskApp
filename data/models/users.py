import sqlalchemy as sa
from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column('id', sa.Integer, autoincrement=True, primary_key=True)
    surname = sa.Column('surname', sa.String, nullable=True)
    name = sa.Column('name', sa.String, nullable=True)
    lessons_list = sa.Column('lessons_list', sa.String, nullable=True)
    birth_date = sa.Column('birth_date', sa.Date, nullable=True)
    in_class = sa.Column('class', sa.Integer, nullable=True)
    about = sa.Column('about', sa.String, nullable=True)
    email = sa.Column('email', sa.String, nullable=True, unique=True)
    password = sa.Column('password', sa.String, nullable=True)

    lessons = sa.orm.relation("Lessons", back_populates='users')
