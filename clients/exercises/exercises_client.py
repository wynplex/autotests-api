import allure
from httpx import Response

from clients.api_client import APIClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, GetExerciseResponseSchema, \
	GetExercisesQuerySchema, \
	GetExercisesResponseSchema, UpdateExerciseRequestSchema
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client



class ExercisesClient(APIClient):
	"""
    Клиент для работы с /api/v1/exercises
    """

	@allure.step("Get exercises in course")
	def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
		"""
        Метод получения списка заданий.

        :param query: Query параметр с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.get("/api/v1/exercises", params=query.model_dump(by_alias=True))

	@allure.step("Get exercise by id {exercise_id}")
	def get_exercise_api(self, exercise_id: str) -> Response:
		"""
        Метод получения одного задания.

        :param exercise_id: ID задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.get(f"/api/v1/exercises/{exercise_id}")

	@allure.step("Create exercise")
	def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
		"""
        Метод создания задания.

        :param request: Данные для создания задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.post("/api/v1/exercises", json=request.model_dump(by_alias=True))

	@allure.step("Update exercise by id {exercise_id}")
	def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
		"""
        Метод обновления задания.

        :param exercise_id: ID задания.
        :param request: Данные для обновления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.patch(f"/api/v1/exercises/{exercise_id}", json=request.model_dump(by_alias=True))

	@allure.step("Delete exercise by id {exercise_id}")
	def delete_exercise_api(self, exercise_id: str) -> Response:
		"""
        Метод удаления задания.

        :param exercise_id: ID задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.delete(f"/api/v1/exercises/{exercise_id}")

	def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
		"""
        Получение одного задания с парсингом JSON.

        :param exercise_id: ID задания.
        :return: {"exercise": {...}}
        """
		response = self.get_exercise_api(exercise_id)
		return GetExerciseResponseSchema.model_validate_json(response.text)

	def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
		"""
        Получение списка заданий с парсингом JSON.

        :param query: Query параметры.
        :return: {"exercises": [{...}, {...}]}
        """
		response = self.get_exercises_api(query)
		return GetExercisesResponseSchema.model_validate_json(response.text)

	def create_exercise(self, request: CreateExerciseRequestSchema) -> GetExerciseResponseSchema:
		"""
        Создание задания с парсингом JSON.

        :param request: Данные для создания.
        :return: {"exercise": {...}}
        """
		response = self.create_exercise_api(request)
		return GetExerciseResponseSchema.model_validate_json(response.text)


	def update_exercise(
			self,
			exercise_id: str,
			request: UpdateExerciseRequestSchema
	) -> GetExerciseResponseSchema:
		"""
        Обновление задания с парсингом JSON.

        :param exercise_id: ID задания.
        :param request: Данные для обновления.
        :return: {"exercise": {...}}
        """
		response = self.update_exercise_api(exercise_id, request)
		return GetExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
	"""
    Билдер для ExercisesClient с авторизацией.

    :param user: Данные пользователя с токеном.
    :return: Настроенный клиент.
    """
	return ExercisesClient(client=get_private_http_client(user))