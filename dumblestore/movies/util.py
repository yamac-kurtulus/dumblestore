import json
import requests


f = open("./MOCK_DATA.json")
data = json.load(f)

users = [
    {
        "first_name": movie["first_name"],
        "last_name": movie["last_name"],
        "password": movie["first_name"] + "42",
        "email": movie["email"],
    }
    for movie in data
]
movies = [
    {"title": movie["Movie Title"], "genres": movie["Movie Genres"].split("|")}
    for movie in data
]

base_url = "https://dumblestore.herokuapp.com"
cred = {"username": "albus@hogwarts.com", "password": "kendra1881"}
token_req = requests.post(f"{base_url}/api-token-auth/", data=cred)

token = "Token " + token_req.json()["token"]
r = requests.get("f"{base_url}"/api/movies", headers={"Authorization": token})

for user in users:
    user_req = requests.post(
        "f"{base_url}"/api/users/",
        headers={"Authorization": token, "content-type": "application/json"},
        data=json.dumps(user),
    )

for movie in movies:
    movie_req = (
        requests.post(
            "http://localhost:8000/api/movies.json/",
            headers={"Authorization": token, "content-type": "application/json"},
            data=json.dumps(movie),
        ),
    )

print(movie_req.json(), user_req.json())
