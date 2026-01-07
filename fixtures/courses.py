import pytest
from pydantic import BaseModel

from clients.courses.courses_client import CoursesClient, get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.files import FilesFixture
from fixtures.users import UserFixture


class CoursesFixture(BaseModel):
	request: CreateCourseRequestSchema
	response: CreateCourseResponseSchema


@pytest.fixture
def courses_clien(function_user: UserFixture) -> CoursesClient:
	return get_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(courses_client: CoursesClient, function_user: UserFixture,
					function_file: FilesFixture) -> CoursesFixture:
	request = CreateCourseRequestSchema()
	response = courses_client.create_course(request)
	return CoursesFixture(request=request, response=response)
