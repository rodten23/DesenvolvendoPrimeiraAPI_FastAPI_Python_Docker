from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.centro_treinamento.schemas__centro_trei import CentrosTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models_centro_trei import CentrosTreinamentoModel

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)

async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentrosTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentrosTreinamentoModel(**centro_treinamento_out.model_dump())
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out

@router.get(
    '/',
    summary='Consulta todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut]
)

async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centro_treinamento_out: list[CentroTreinamentoOut] = (await db_session.execute(select(CentrosTreinamentoModel))).scalars().all()

    return centro_treinamento_out

@router.get(
    '/{id}',
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut
)

async def query(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut = (await db_session.execute(select(CentrosTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro_treinamento_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )

    return centro_treinamento_out
