from .investment import Investment
from sqlalchemy import Column, Text, String


class CharityProject(Investment):
    description = Column(Text, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
