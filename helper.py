import requests

'''
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/classes").json())
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/teachers").json())
print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/classes", json={"title": "105"}).json())
'''
print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/students", json={"surname": "student_surname1",
                                                                                    "name": "student_name1",
                                                                                    "birth_date": "2000-01-01",
                                                                                    "email": "test_student1@mail.ru",
                                                                                    "password": "123",
                                                                                    "role": "Student",
                                                                                    "in_class": "105"}).json())
"""
print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/teachers", json={"surname": "teachers_surname",
                                                                                    "name": "teachers_name",
                                                                                    "birth_date": "1999-01-01",
                                                                                    "email": "test_teacher@mail.ru",
                                                                                    "password": "123",
                                                                                    "role": "Teacher",
                                                                                    "taught_subject": 1,
                                                                                    "a_class": "105"}).json())
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/teachers").json())
print(requests.get("https://pure-spire-34349.herokuapp.com/api/v1/students").json())
"""