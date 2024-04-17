from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = "forbid"


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectDB(CharityProjectBase):
    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        exclude_unset = True
