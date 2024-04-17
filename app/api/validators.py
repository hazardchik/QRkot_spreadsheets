from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
    charity_project_with_name_id: int = None,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id not in [charity_project_with_name_id, None]:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Проект с таким именем уже существует!"
        )


async def check_charity_project_before_delete(
    charity_project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if not charity_project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден!")

    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    return charity_project


async def check_charity_project_before_edit(
    charity_project_id: int,
    new_charity_project: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    await check_name_duplicate(new_charity_project.name, session, charity_project_id)
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )

    if not charity_project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Проект не найден!")

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Закрытый проект нельзя редактировать!"
        )

    if (
        new_charity_project.full_amount and
        charity_project.invested_amount > new_charity_project.full_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Требуемая сумма не может быть меньше внесенной!",
        )

    return charity_project
