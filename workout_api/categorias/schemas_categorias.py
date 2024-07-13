from pydantic import UUID4, Field
from typing import Annotated
from workout_api.contrib.schemas_contrib import BaseSchema

class CategoriasIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]

class CategoriasOut(CategoriasIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]
