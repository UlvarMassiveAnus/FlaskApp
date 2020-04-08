import sqlalchemy as sa
from data.db_session import SqlAlchemyBase


class Teachers(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sa.Column('id', sa.Integer, nullable=True, autoincrement=True, primary_key=True)
    surname = sa.Column('surname', sa.String, nullable=True)
    name = sa.Column('name', sa.String, nullable=True)
    taught_subject = sa.Column('taught_subject', sa.Integer, sa.ForeignKey("subjects.id"), nullable=True)
    birth_date = sa.Column('birth_date', sa.Date, nullable=True)
    about = sa.Column('about', sa.String, nullable=True)
    email = sa.Column('email', sa.String, nullable=True)
    password = sa.Column('password', sa.String, nullable=True)

    lessons = sa.orm.relation("Lessons", back_populates='teachers')
    subjects = sa.orm.relation("Subjects", back_populates='teachers')