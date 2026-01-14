from pydantic import BaseModel, EmailStr, Field, constr

from tools.fakers import fake


class UserSchema(BaseModel):
	id: str
	email: EmailStr = Field(default_factory=fake.email)
	lastName: constr(min_length=1, max_length=50)
	firstName: constr(min_length=1, max_length=50)
	middleName: constr(min_length=1, max_length=50)


class CreateUserRequestSchema(BaseModel):
	email: EmailStr = Field(default_factory=fake.email)
	password: constr(min_length=1, max_length=250)
	lastName: constr(min_length=1, max_length=50)
	firstName: constr(min_length=1, max_length=50)
	middleName: constr(min_length=1, max_length=50)


class CreateUserResponseSchema(BaseModel):
	user: UserSchema
