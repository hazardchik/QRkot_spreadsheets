from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime

from app.core.db import Base


class Investment(Base):
    __abstract__ = True

    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime)

    def close(self):
        if not (self.fully_invested and self.close_date):
            self.close_date = datetime.now()
            self.fully_invested = True
