from pydantic import BaseModel, ConfigDict, Field

from tools.fakers import fake


class GetExercisesQuerySchema(BaseModel):
	"""
    Параметр запроса для получения списка заданий курса.
    """
	model_config = ConfigDict(populate_by_name=True)  # ← Добавь эту строку!

	course_id: str = Field(alias="courseId")

class CreateExerciseRequestSchema(BaseModel):
	"""
    Данные для создания нового задания.
    """
	model_config = ConfigDict(populate_by_name=True)

	title: str = Field(default_factory=fake.sentence)
	course_id: str = Field(alias="courseId", default_factory=fake.uuid4)
	max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
	min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
	order_index: int = Field(alias="orderIndex", default_factory=fake.integer)
	description: str = Field(default_factory=fake.text)
	estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)


class UpdateExerciseRequestSchema(BaseModel):
	"""
    Данные для обновления задания (все поля опциональные).
    """
	model_config = ConfigDict(populate_by_name=True)

	title: str | None = Field(default_factory=fake.sentence)
	max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
	min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
	order_index: int = Field(alias="orderIndex", default_factory=fake.integer)
	description: str | None = Field(default_factory=fake.text)
	estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)

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

class UpdateExerciseResponseSchema(BaseModel):
	"""Схема запроса на обновление задания"""
	exercise: ExerciseSchema

class GetExercisesResponseSchema(BaseModel):
	"""
    Ответ для GET /api/v1/exercises
    Возвращает СПИСОК exercises
    """
	exercises: list[ExerciseSchema]

class CreateExerciseResponseSchema(BaseModel):
	"""
	Ответ для POST /api/v1/exercises
	Возвращает ОДИН exercise
	"""
	exercise: ExerciseSchema