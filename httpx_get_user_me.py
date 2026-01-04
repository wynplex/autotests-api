import httpx


client = httpx.Client(
	base_url="http://localhost:8000"
)
auth_info = {
  "email": "user@example.com",
  "password": "string"
}

response = client.post("/api/v1/authentication/login", json=auth_info)

headers = {
	"Authorization": f"Bearer {response.json()["token"]["accessToken"]}"
}
response = client.get("/api/v1/users/me", headers = headers)
print(response.status_code)
print(response.json())
