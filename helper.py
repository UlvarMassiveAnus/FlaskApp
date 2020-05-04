from data.db_session import create_session, global_init
from data.models.lessons import Lessons
import datetime

global_init("db/project.sqlite")
session = create_session()
lesson = session.query(Lessons).get(3)