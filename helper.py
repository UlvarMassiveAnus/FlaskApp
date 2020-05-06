from data.db_session import create_session, global_init
from data.models.teachers import Teachers
from data.models.a_class import AClasses
import datetime

global_init("db/project.sqlite")
session = create_session()
t = session.query(AClasses).get(1)
print(t.teachers.users.name)