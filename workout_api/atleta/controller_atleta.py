from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from uuid import uuid4
from workout_api.atleta.schemas_atletas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models_categorias import CategoriasModel
from workout_api.centro_treinamento.models_centro_trei import CentrosTreinamentoModel
from workout_api.atleta.models_atleta import AtletasModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model = AtletaOut
)

async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriasModel).filter_by(nome=categoria_nome))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada'
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentrosTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento} não foi encontrado'
        )
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())

        atleta_model = AtletasModel(**atleta_out.model_dump(exclude={'categoria', 'centro de treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu erros ao receber dados no banco.'
        )

    return atleta_out

@router.get(
    '/',
    summary='Consulta todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut]
)

async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas_out: list[AtletaOut] = (await db_session.execute(select(AtletasModel))).scalars().all()

    return [AtletaOut.model_validate(atletas_out) for atletas in atletas_out]

@router.get(
    '/{id}',
    summary='Consulta um(a) atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)

async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta_out: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(id=id))).scalars().first()

    if not atleta_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) no id: {id}'
        )

    return atleta_out

@router.patch(
    '/{id}',
    summary='Editar um(a) atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)

async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta_out: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(id=id))).scalars().first()

    if not atleta_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) no id: {id}'
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta_out, key, value)

    await db.session.commit()
    await db.session.refresh(atleta_out)

    return atleta_out

@router.delete(
    '/{id}',
    summary='Excluir um(a) atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)

async def query(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta_out: AtletaOut = (await db_session.execute(select(AtletasModel).filter_by(id=id))).scalars().first()

    if not atleta_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado(a) no id: {id}'
        )
    
    await db.session.delete(atleta_out)
    await db.session.commit()
