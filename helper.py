import requests

print(requests.post("http://127.0.0.1:5000/api/v1/students", json={"surname": "Sidorov",
                                                                   "name": "Sidor",
                                                                   "birth_date": "2003-05-09",
                                                                   "email": "sidorov@mail.ru",
                                                                   "password": "123123",
                                                                   "role": "Student",
                                                                   "in_class": 1}).json())