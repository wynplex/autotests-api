import allure

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import (
	CreateExerciseRequestSchema,
	CreateExerciseResponseSchema,
	ExerciseSchema,
	GetExerciseResponseSchema,
	GetExercisesResponseSchema,
	UpdateExerciseRequestSchema,
	UpdateExerciseResponseSchema
)
from tools.assertions.base import assert_equal
from tools.assertions.errors import assert_internal_error_response


def assert_create_exercise_response(
		request: CreateExerciseRequestSchema,
		response: CreateExerciseResponseSchema
):
	"""
    Проверяет что ответ на создание задания соответствует данным из запроса.

    :param request: Исходный запрос на создание задания.
    :param response: Ответ API с данными созданного задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
	with allure.step("Verify created exercise matches request data"):
		assert_equal(response.exercise.title, request.title, "title")
		assert_equal(response.exercise.course_id, request.course_id, "course_id")
		assert_equal(response.exercise.max_score, request.max_score, "max_score")
		assert_equal(response.exercise.min_score, request.min_score, "min_score")
		assert_equal(response.exercise.order_index, request.order_index, "order_index")
		assert_equal(response.exercise.description, request.description, "description")
		assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
	"""
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания.
    :param expected: Ожидаемые данные задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
	with allure.step(f"Verify exercise data matches (id: {expected.id})"):
		assert_equal(actual.id, expected.id, "id")
		assert_equal(actual.title, expected.title, "title")
		assert_equal(actual.course_id, expected.course_id, "course_id")
		assert_equal(actual.max_score, expected.max_score, "max_score")
		assert_equal(actual.min_score, expected.min_score, "min_score")
		assert_equal(actual.order_index, expected.order_index, "order_index")
		assert_equal(actual.description, expected.description, "description")
		assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


def assert_get_exercise_response(
		get_response: GetExerciseResponseSchema,
		create_response: CreateExerciseResponseSchema
):
	"""
    Проверяет, что данные задания при GET-запросе соответствуют данным при создании.

    :param get_response: Ответ API на GET-запрос задания.
    :param create_response: Ответ API на создание задания (из фикстуры).
    :raises AssertionError: Если данные не совпадают.
    """
	with allure.step("Verify GET response matches created exercise"):
		assert_exercise(
			actual=get_response.exercise,
			expected=create_response.exercise
		)


def assert_update_exercise_response(
		request: UpdateExerciseRequestSchema,
		response: UpdateExerciseResponseSchema
):
	"""
    Проверяет, что ответ на обновление задания соответствует данным из запроса.

    :param request: Исходный запрос на обновление задания.
    :param response: Ответ API с обновленными данными задания.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
	with allure.step("Verify updated exercise matches request data"):
		if request.title is not None:
			assert_equal(response.exercise.title, request.title, "title")

		if request.max_score is not None:
			assert_equal(response.exercise.max_score, request.max_score, "max_score")

		if request.min_score is not None:
			assert_equal(response.exercise.min_score, request.min_score, "min_score")

		if request.order_index is not None:
			assert_equal(response.exercise.order_index, request.order_index, "order_index")

		if request.description is not None:
			assert_equal(response.exercise.description, request.description, "description")

		if request.estimated_time is not None:
			assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


def assert_exercise_not_found_response(response: InternalErrorResponseSchema):
	"""
    Проверяет, что API вернул ошибку 'Exercise not found'.

    :param response: Ответ API с внутренней ошибкой.
    :raises AssertionError: Если сообщение об ошибке не соответствует ожидаемому.
    """
	with allure.step("Verify error message: 'Exercise not found'"):
		expected = InternalErrorResponseSchema(details="Exercise not found")
		assert_internal_error_response(actual=response, expected=expected)

def assert_get_exercises_response(
		get_response: GetExercisesResponseSchema,
		created_exercises: list[CreateExerciseResponseSchema]
):
	"""
	Проверяет, что список заданий содержит все созданные задания.

	:param get_response: Ответ API на GET-запрос списка заданий.
	:param created_exercises: Список созданных заданий для сравнения.
	:raises AssertionError: Если данные не совпадают.
	"""
	expected_count = len(created_exercises)
	actual_count = len(get_response.exercises)

	with allure.step(f"Verify exercises count: {actual_count} == {expected_count}"):
		assert actual_count == expected_count, (
			f"Expected {expected_count} exercises, but got {actual_count}"
		)

	created_by_id = {ex.exercise.id: ex.exercise for ex in created_exercises}

	with allure.step(f"Verify all {actual_count} exercises match created data"):
		for exercise in get_response.exercises:
			with allure.step(f"Exercise: {exercise.title}..."):
				assert exercise.id in created_by_id, (
					f"Exercise with id={exercise.id} not found in created exercises"
				)

				expected_exercise = created_by_id[exercise.id]
				assert_exercise(actual=exercise, expected=expected_exercise)