import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, GetExerciseResponseSchema
from fixtures.users import UserFixture


class ExerciseFixture(BaseModel):
	request: CreateExerciseRequestSchema
	response: GetExerciseResponseSchema

@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
	return get_exercises_client(function_user.authentication_user)

@pytest.fixture # по дефолту scope=function
def function_exercise(exercises_client: ExercisesClient) -> ExerciseFixture:
	request = CreateExerciseRequestSchema()
	response = exercises_client.create_exercise(request)
	return ExerciseFixture(request=request, response=response)