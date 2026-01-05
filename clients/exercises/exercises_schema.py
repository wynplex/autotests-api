from pydantic import BaseModel, ConfigDict, Field


class GetExercisesQuerySchema(BaseModel):
	"""
    Параметр запроса для получения списка заданий курса.
    """
	course_id: str = Field(alias="courseId")

class CreateExerciseRequestSchema(BaseModel):
	"""
    Данные для создания нового задания.
    """
	model_config = ConfigDict(populate_by_name=True)

	title: str
	course_id: str = Field(alias="courseId")
	max_score: int | None = Field(alias="maxScore")
	min_score: int | None = Field(alias="minScore")
	order_index: int = Field(alias="orderIndex")
	description: str
	estimated_time: str | None = Field(alias="estimatedTime")


class UpdateExerciseRequestSchema(BaseModel):
	"""
    Данные для обновления задания (все поля опциональные).
    """
	model_config = ConfigDict(populate_by_name=True)

	title: str | None
	max_score: int | None = Field(alias="maxScore")
	min_score: int | None = Field(alias="minScore")
	order_index: int = Field(alias="orderIndex")
	description: str | None
	estimated_time: str | None = Field(alias="estimatedTime")

class ExerciseSchema(BaseModel):
	"""
    Структура объекта Exercise из API.
    Соответствует схеме Exercise в swagger.
    """
	model_config = ConfigDict(populate_by_name=True)

	id: str
	title: str
	course_id: str = Field(alias="courseId")
	max_score: int | None = Field(alias="maxScore")
	min_score: int | None = Field(alias="minScore")
	order_index: int = Field(alias="orderIndex")
	description: str
	estimated_time: str | None = Field(alias="estimatedTime")

class GetExerciseResponseSchema(BaseModel):
	"""
    Ответ для GET /api/v1/exercises/{exercise_id}
    Возвращает ОДИН exercise
    """
	exercise: ExerciseSchema


class GetExercisesResponseSchema(BaseModel):
	"""
    Ответ для GET /api/v1/exercises
    Возвращает СПИСОК exercises
    """
	exercises: list[ExerciseSchema]
