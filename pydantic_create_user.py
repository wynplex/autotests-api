from pydantic import BaseModel, EmailStr, constr


class UserSchema(BaseModel):
	id: str
	email: EmailStr
	lastName: constr(min_length=1, max_length=50)
	firstName: constr(min_length=1, max_length=50)
	middleName: constr(min_length=1, max_length=50)


class CreateUserRequestSchema(BaseModel):
	email: EmailStr
	password: constr(min_length=1, max_length=250)
	lastName: constr(min_length=1, max_length=50)
	firstName: constr(min_length=1, max_length=50)
	middleName: constr(min_length=1, max_length=50)


class CreateUserResponseSchema(BaseModel):
	user: UserSchema
