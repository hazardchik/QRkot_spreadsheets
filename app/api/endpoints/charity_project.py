from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import execute_investment_process

from app.api.validators import (
    check_name_duplicate,
    check_charity_project_before_edit,
    check_charity_project_before_delete
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получить все благотворительные проекты.
    """
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Создать новый благотворительный проект (только для суперюзеров).
    """
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    new_charity_project = await execute_investment_process(new_charity_project, session)
    return new_charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновить благотворительный проект (только для суперюзеров).
    """
    charity_project = await check_charity_project_before_edit(
        charity_project_id, obj_in, session
    )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session,
    )
    charity_project = await execute_investment_process(charity_project, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить благотворительный проект (только для суперюзеров).
    """
    charity_project = await check_charity_project_before_delete(
        charity_project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
