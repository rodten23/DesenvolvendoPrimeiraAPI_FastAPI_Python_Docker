from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.schemas_categorias import CategoriasIn, CategoriasOut
from workout_api.categorias.models_categorias import CategoriasModel

router = APIRouter()

@router.post(
    '/',
    summary='Criar uma nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriasOut
)

async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriasIn = Body(...)
) -> CategoriasOut:
    categoria_out = CategoriasOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriasModel(**categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out

@router.get(
    '/',
    summary='Consulta todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriasOut]
)

async def query(db_session: DatabaseDependency) -> list[CategoriasOut]:
    categorias_out: list[CategoriasOut] = (await db_session.execute(select(CategoriasModel))).scalars().all()

    return categorias_out

@router.get(
    '/{id}',
    summary='Consulta uma categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriasOut
)

async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriasOut:
    categoria_out: CategoriasOut = (await db_session.execute(select(CategoriasModel).filter_by(id=id))).scalars().first()

    if not categoria_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria não encontrada no id: {id}'
        )

    return categoria_out
