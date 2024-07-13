from pydantic import Field, PositiveFloat
from typing import Annotated, Optional
from workout_api.categorias.schemas_categorias import CategoriasIn
from workout_api.centro_treinamento.schemas__centro_trei import CentroTreinamentoAtleta
from workout_api.contrib.schemas_contrib import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do(a) atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do(a) atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do(a) atleta', example=23, max_length=3)]
    peso: Annotated[PositiveFloat, Field(description='Peso do(a) atleta', example=90.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do(a) atleta', example=1.80)]
    genero: Annotated[str, Field(description='Gênero do(a) atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriasIn, Field(description='Categoria do(a) atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do(a) atleta')]

class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do(a) atleta', example='João', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do(a) atleta', example=23, max_length=3)]
