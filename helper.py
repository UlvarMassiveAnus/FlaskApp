from data.db_session import global_init, create_session
from data.models.users import Users
from data.models.students import Students


global_init("db/project.sqlite")
'''
session = create_session()
user = 
shadow = Students(
    user_id=user.id
)
user.shadow = shadow
session.add(shadow)
session.commit()
'''
session = create_session()
user = session.query(Users).filter(Users.email == "asasa").first()
student = session.query(Students).filter(Students.user_id == user.id).first()
user.shadow = student

print(user.shadow)