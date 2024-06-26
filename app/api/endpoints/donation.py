from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDB, DonationUser
)
from app.models import User

from app.services.investment import execute_investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получить все пожертвования (только для суперпользователей).
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationUser],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получить пожертвования пользователя.
    """
    user_donations = await donation_crud.get_by_user(session, user)
    return user_donations


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Создать пожертвование.
    """
    new_donation = await donation_crud.create(
        donation, session, user
    )
    new_donation = await execute_investment_process(new_donation, session)
    return new_donation
