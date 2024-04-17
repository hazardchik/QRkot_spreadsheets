from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):
    async def get_charity_project_id_by_name(
            self,
            charity_project: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
