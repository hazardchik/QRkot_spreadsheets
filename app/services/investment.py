from typing import List, Union
from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject, Donation


async def get_not_invested_objects(
    model: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    query = select(model).where(
        model.fully_invested == false()
    ).order_by(model.create_date)
    return (await session.execute(query)).scalars().all()


async def close_invested_object(obj_to_close: Union[CharityProject, Donation]) -> None:
    obj_to_close.close()


async def execute_investment_process(
    object_in: Union[CharityProject, Donation],
    session: AsyncSession
):
    db_model = CharityProject if isinstance(object_in, Donation) else Donation
    not_invested_objects = await get_not_invested_objects(db_model, session)
    available_amount = object_in.full_amount

    for not_invested_obj in not_invested_objects:
        need_to_invest = not_invested_obj.full_amount - not_invested_obj.invested_amount
        to_invest = min(need_to_invest, available_amount)
        not_invested_obj.invested_amount += to_invest
        object_in.invested_amount += to_invest
        available_amount -= to_invest

        if not_invested_obj.full_amount == not_invested_obj.invested_amount:
            not_invested_obj.close()

        if not available_amount:
            object_in.close()
            break

    await session.commit()
    await session.refresh(object_in)
    return object_in
