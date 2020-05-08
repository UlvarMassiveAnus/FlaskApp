import requests

print(requests.get("http://127.0.0.1:5000/api/v1/teachers").json())
print(requests.get("http://127.0.0.1:5000/api/v1/students").json())
print(requests.delete("http://127.0.0.1:5000/api/v1/users/4").json())