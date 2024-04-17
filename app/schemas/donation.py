from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DonationBase(BaseModel):
    comment: Optional[str] = None
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = "forbid"


class DonationCreate(DonationBase):
    pass


class DonationUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationUser):
    invested_amount: int
    fully_invested: bool
    user_id: int
