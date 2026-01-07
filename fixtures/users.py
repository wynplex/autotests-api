import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
	request: CreateUserRequestSchema
	response: CreateUserResponseSchema
	authentication_user: AuthenticationUserSchema

	@property
	def email(self) -> EmailStr:  # Быстрый доступ к email пользователя
		return self.request.email

	@property
	def password(self) -> str:  # Быстрый доступ к password пользователя
		return self.request.password


@pytest.fixture
def public_users_client() -> PublicUsersClient:
	return get_public_users_client()


@pytest.fixture
def private_users_client(function_user) -> PrivateUsersClient:
	"""Фикстура приватного клиента пользователей с аутентификацией"""
	return get_private_users_client(user=function_user.authentication_user)


@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
	request = CreateUserRequestSchema()
	response = public_users_client.create_user(request)

	auth_user = AuthenticationUserSchema(
		email=request.email,
		password=request.password
	)

	return UserFixture(request=request, response=response, authentication_user=auth_user)
