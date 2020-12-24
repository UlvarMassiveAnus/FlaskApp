import requests

print(requests.post("http://localhost:5000/api/v1/classes", json={"key": "secret_key",
                                                                  "title": "101"}).json())

print(requests.post("http://localhost:5000/api/v1/teachers", json={"key": "secret_key",
                                                                   "name": "Sidor",
                                                                   "surname": "Sidorov",
                                                                   "birth_date": "2010-01-01",
                                                                   "email": "sidorov@mail.ru",
                                                                   "password": "123",
                                                                   "role": "Teacher",
                                                                   "taught_subject": 1,
                                                                   "a_class": "101"}).json())

print(requests.post("http://localhost:5000/api/v1/students", json={"key": "secret_key",
                                                                   "name": "Ivan",
                                                                   "surname": "Ivanov",
                                                                   "birth_date": "2000-01-01",
                                                                   "email": "ivanov@mail.ru",
                                                                   "password": "123",
                                                                   "role": "Student",
                                                                   "in_class": "101"}).json())
'''
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/classes").json())
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/teachers").json())
print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/classes", json={"key": "secret_key",
                                                                                   "title": "105"}).json())

print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/students", json={"key": "secret_key",
                                                                                    "surname": "student_surname1",
                                                                                    "name": "student_name1",
                                                                                    "birth_date": "2000-01-01",
                                                                                    "email": "test_student1@mail.ru",
                                                                                    "password": "123",
                                                                                    "role": "Student",
                                                                                    "in_class": "101"}).json())
# Теперь мы можем под таким email и паролем войти в систему как ученик
print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/teachers", json={"key": "secret_key",
                                                                                    "surname": "teachers_surname",
                                                                                    "name": "teachers_name",
                                                                                    "birth_date": "1999-01-01",
                                                                                    "email": "test_teacher@mail.ru",
                                                                                    "password": "123",
                                                                                    "role": "Teacher",
                                                                                    "taught_subject": 1,
                                                                                    "a_class": "105"}).json())
# Теперь мы можем под таким email и паролем войти в систему как учитель

print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/teachers").json())
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/students").json())
'''