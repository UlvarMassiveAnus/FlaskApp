from data.db_session import create_session, global_init
from data.models.teachers import Teachers
from data.models.a_class import AClasses
import datetime
from data.models.lessons import Lessons

global_init("db/project.sqlite")
session = create_session()
t = session.query(Lessons).get(10)
print(t.lesson_date)