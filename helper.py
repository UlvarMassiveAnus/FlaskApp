import requests

# print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/classes", json={"title": "103"}))
print(requests.post("https://pure-spire-34349.herokuapp.com/api/v1/teachers", json={"surname": "Sidorov",
                                                                                    "name": "Sidor",
                                                                                    "birth_date": "2003-05-09",
                                                                                    "email": "sidorov@mail.ru",
                                                                                    "password": "123123",
                                                                                    "role": "Teacher",
                                                                                    "taught_subject": 1,
                                                                                    "a_class": "103"}).json())
