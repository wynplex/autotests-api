import httpx

from tools.fakers import fake


client = httpx.Client(base_url="http://localhost:8000")

payload = {
    "email": fake.email(),
    "password": "password",
    "lastName": "Ivanov",
    "firstName": "Ivan",
    "middleName": "Ivanovich"
}

create_user_response = client.post("/api/v1/users", json=payload)
create_user_response.raise_for_status()

login_payload = {
    "email": payload["email"],
    "password": payload["password"]
}
get_jwt_response = client.post("/api/v1/authentication/login", json=login_payload)
get_jwt_response.raise_for_status()

access_token = get_jwt_response.json()["token"]["accessToken"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

patch_payload = {
    "email": get_random_email(),
    "lastName": "Petrov",
    "firstName": "Petr",
    "middleName": "Petrovich"
}

user_id = create_user_response.json()["user"]["id"]
patch_response = client.patch(
    f"/api/v1/users/{user_id}",
    headers=headers,
    json=patch_payload
)
patch_response.raise_for_status()