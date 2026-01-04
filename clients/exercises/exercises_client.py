from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class GetExercisesQueryDict(TypedDict):
	"""
    Параметр запроса для получения списка заданий курса.
    """
	courseId: str

class CreateExerciseRequestDict(TypedDict):
	"""
    Данные для создания нового задания.
    """
	title: str
	courseId: str
	maxScore: int | None
	minScore: int | None
	orderIndex: int
	description: str
	estimatedTime: str | None


class UpdateExerciseRequestDict(TypedDict):
	"""
    Данные для обновления задания (все поля опциональные).
    """
	title: str | None
	maxScore: int | None
	minScore: int | None
	orderIndex: int | None
	description: str | None
	estimatedTime: str | None

class ExerciseDict(TypedDict):
	"""
    Структура объекта Exercise из API.
    Соответствует схеме Exercise в swagger.
    """
	id: str
	title: str
	courseId: str
	maxScore: int | None
	minScore: int | None
	orderIndex: int
	description: str
	estimatedTime: str | None

class GetExerciseResponseDict(TypedDict):
	"""
    Ответ для GET /api/v1/exercises/{exercise_id}
    Возвращает ОДИН exercise
    """
	exercise: ExerciseDict


class GetExercisesResponseDict(TypedDict):
	"""
    Ответ для GET /api/v1/exercises
    Возвращает СПИСОК exercises
    """
	exercises: list[ExerciseDict]

class ExercisesClient(APIClient):
	"""
    Клиент для работы с /api/v1/exercises
    """

	def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
		"""
        Метод получения списка заданий.

        :param query: Query параметр с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.get("/api/v1/exercises", params=query)

	def get_exercise_api(self, exercise_id: str) -> Response:
		"""
        Метод получения одного задания.

        :param exercise_id: ID задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.get(f"/api/v1/exercises/{exercise_id}")

	def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
		"""
        Метод создания задания.

        :param request: Данные для создания задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.post("/api/v1/exercises", json=request)

	def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
		"""
        Метод обновления задания.

        :param exercise_id: ID задания.
        :param request: Данные для обновления.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

	def delete_exercise_api(self, exercise_id: str) -> Response:
		"""
        Метод удаления задания.

        :param exercise_id: ID задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
		return self.delete(f"/api/v1/exercises/{exercise_id}")

	def get_exercise(self, exercise_id: str) -> GetExerciseResponseDict:
		"""
        Получение одного задания с парсингом JSON.

        :param exercise_id: ID задания.
        :return: {"exercise": {...}}
        """
		return self.get_exercise_api(exercise_id).json()

	def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
		"""
        Получение списка заданий с парсингом JSON.

        :param query: Query параметры.
        :return: {"exercises": [{...}, {...}]}
        """
		return self.get_exercises_api(query).json()

	def create_exercise(self, request: CreateExerciseRequestDict) -> GetExerciseResponseDict:
		"""
        Создание задания с парсингом JSON.

        :param request: Данные для создания.
        :return: {"exercise": {...}}
        """
		return self.create_exercise_api(request).json()

	def update_exercise(
			self,
			exercise_id: str,
			request: UpdateExerciseRequestDict
	) -> GetExerciseResponseDict:
		"""
        Обновление задания с парсингом JSON.

        :param exercise_id: ID задания.
        :param request: Данные для обновления.
        :return: {"exercise": {...}}
        """
		return self.update_exercise_api(exercise_id, request).json()


def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
	"""
    Билдер для ExercisesClient с авторизацией.

    :param user: Данные пользователя с токеном.
    :return: Настроенный клиент.
    """
	return ExercisesClient(client=get_private_http_client(user))