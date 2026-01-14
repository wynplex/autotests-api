import pytest
from pydantic import BaseModel

from clients.files.files_client import FilesClient, get_files_client
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from config import settings
from fixtures.users import UserFixture


class FilesFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema


@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(function_user.authentication_user)


@pytest.fixture
def function_file(files_client: FilesClient) -> FilesFixture:
    request = CreateFileRequestSchema(upload_file=settings.test_data.image_png_file)
    response = files_client.create_file(request)
    return FilesFixture(request=request, response=response)
