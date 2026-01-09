from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
	GetExerciseResponseSchema, GetExercisesQuerySchema, GetExercisesResponseSchema, UpdateExerciseRequestSchema, \
	UpdateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_exercise_not_found_response, \
	assert_get_exercise_response, \
	assert_get_exercises_response, assert_update_exercise_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
class TestExercises:

	@allure.tag(AllureTag.CREATE_ENTITY)
	@allure.story(AllureStory.CREATE_ENTITY)
	@allure.severity(Severity.BLOCKER)
	@allure.title("Create exercise")
	def test_create_exercise(
			self,
			exercises_client: ExercisesClient,
			function_course: CourseFixture
	):
		request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
		response = exercises_client.create_exercise_api(request)
		response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

		assert_status_code(response.status_code, HTTPStatus.OK)
		assert_create_exercise_response(request, response_data)
		validate_json_schema(response.json(), response_data.model_json_schema())

	@allure.tag(AllureTag.GET_ENTITY)
	@allure.story(AllureStory.GET_ENTITY)
	@allure.severity(Severity.BLOCKER)
	@allure.title("Get exercise")
	def test_get_exercise(
			self,
			exercises_client: ExercisesClient,
			function_exercise: ExerciseFixture
	):
		"""Тест получения задания по ID через API"""
		response = exercises_client.get_exercise_api(exercise_id=function_exercise.response.exercise.id)
		response_data = GetExerciseResponseSchema.model_validate_json(response.text)

		assert_status_code(response.status_code, HTTPStatus.OK)
		assert_get_exercise_response(
			get_response=response_data,
			create_response=function_exercise.response
		)

		validate_json_schema(
			instance=response.json(),
			schema=GetExerciseResponseSchema.model_json_schema()
		)

	@allure.tag(AllureTag.UPDATE_ENTITY)
	@allure.story(AllureStory.UPDATE_ENTITY)
	@allure.severity(Severity.CRITICAL)
	@allure.title("Update exercise")
	def test_update_exercise(
			self,
			exercises_client: ExercisesClient,
			function_exercise: ExerciseFixture
	):
		"""Тест обновления задания через API"""
		request = UpdateExerciseRequestSchema()
		response = exercises_client.update_exercise_api(
			exercise_id=function_exercise.response.exercise.id,
			request=request
		)
		response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

		assert_status_code(response.status_code, HTTPStatus.OK)
		assert_update_exercise_response(request, response_data)
		validate_json_schema(
			instance=response.json(),
			schema=UpdateExerciseResponseSchema.model_json_schema()
		)

	@allure.tag(AllureTag.DELETE_ENTITY)
	@allure.story(AllureStory.DELETE_ENTITY)
	@allure.severity(Severity.CRITICAL)
	@allure.title("Delete exercise")
	def test_delete_exercise(
			self,
			exercises_client: ExercisesClient,
			function_exercise: ExerciseFixture
	):
		"""Тест удаления задания через API"""
		exercise_id = function_exercise.response.exercise.id
		delete_response = exercises_client.delete_exercise_api(exercise_id=exercise_id)
		get_response = exercises_client.get_exercise_api(exercise_id=exercise_id)
		error_response = InternalErrorResponseSchema.model_validate_json(get_response.text)

		assert_status_code(delete_response.status_code, HTTPStatus.OK)
		assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
		assert_exercise_not_found_response(error_response)

		validate_json_schema(
			instance=get_response.json(),
			schema=InternalErrorResponseSchema.model_json_schema()
		)

	@allure.tag(AllureTag.GET_ENTITIES)
	@allure.story(AllureStory.GET_ENTITIES)
	@allure.severity(Severity.BLOCKER)
	@allure.title("Get exercises")
	def test_get_exercises(
			self,
			exercises_client: ExercisesClient,
			function_course: CourseFixture,
			function_exercise: ExerciseFixture
	):
		"""Тест получения списка заданий через API"""
		# Формируем query-параметры
		query_params = GetExercisesQuerySchema(
			course_id=function_course.response.course.id
		)

		# Отправляем GET-запрос с фильтрацией
		response = exercises_client.get_exercises_api(query_params)

		# Десериализуем ответ
		response_data = GetExercisesResponseSchema.model_validate_json(response.text)

		# Проверяем статус-код
		assert_status_code(response.status_code, HTTPStatus.OK)

		# Проверяем, что в списке есть созданное задание
		assert_get_exercises_response(
			get_response=response_data,
			created_exercises=[function_exercise.response]
		)

		# Валидируем JSON-схему
		validate_json_schema(
			instance=response.json(),
			schema=GetExercisesResponseSchema.model_json_schema()
		)