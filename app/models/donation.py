from sqlalchemy import (
    Column,
    Text,
    Integer,
    ForeignKey,
    CheckConstraint
)
from app.models.investment import Investment


class Donation(Investment):

    comment = Column(Text)

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    )
