from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class CourseIdQuery(TypedDict):
	"""
	Параметр запроса для получения списка заданий курса.
	"""
	courseId: str

class BaseExerciseInfoDict(TypedDict):
	"""
	Базовая информация о задании.
	"""
	title: str
	maxScore: int
	minScore: int
	orderIndex: int
	description: str
	estimatedTime: str

class CreateExerciseRequestDict(BaseExerciseInfoDict):
	"""
	Данные для создания нового задания.
	"""
	courseId: str

class UpdateExerciseRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление задания.
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None

class ExercisesClient(APIClient):
	"""
	Клиент для работы с /api/v1/exercises
	"""

	def get_exercises_api(self, query: CourseIdRequestQuery) -> Response:
		"""
		Метод получения информации о заданиях.

		:param query: Query параметр с course ID.
		:return: Ответ от сервера в виде объекта httpx.Response
		"""
		return self.get("/api/v1/exercises", params=query)

	def get_exercise_api(self, exercise_id: str) -> Response:
		"""
		Метод получения информации о задании.

		:param exercise_id: ID задания о котором необходимо получить информацию.
		:return: Ответ от сервера в виде объекта httpx.Response
		"""
		return self.get(f"/api/v1/exercises/{exercise_id}")

	def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
		"""
		Метод для создания задания.

		:param request: Словарь со всеми необходимыми параметрами для создания задания.
		:return: Ответ от сервера в виде объекта httpx.Response
		"""
		return self.post("/api/v1/exercises", json=request)

	def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
		"""
		Метод для обновления задания.

		:param request: Новая информация о задании.
		:param exercise_id: ID задания.
		:return: Ответ от сервера в виде объекта httpx.Response
		"""
		return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

	def delete_exercise_api(self, exercise_id: str) -> Response:
		"""
		Метод для удаления задания.

		:param exercise_id: ID задания.
		:return: Ответ от сервера в виде объекта httpx.Response
		"""
		return self.delete(f"/api/v1/exercises/{exercise_id}")