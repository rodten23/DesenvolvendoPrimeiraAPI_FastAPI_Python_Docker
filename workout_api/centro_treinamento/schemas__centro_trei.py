from pydantic import Field, UUID4
from typing import Annotated
from workout_api.contrib.schemas_contrib import BaseSchema

class CentrosTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT Lobos', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua dos Uivos, 45', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', example='Rodrigo', max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', exempla='CT Lobos', max_length=20)]

class CentroTreinamentoOut(CentrosTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]
    