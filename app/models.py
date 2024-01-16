from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text, cast
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import INTEGER

class Post(Base):
    __tablename__="alerts"

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String,nullable=False)
    location=Column(String,nullable=False)
    location_link=Column(String,nullable=False)
    published=Column(Boolean,server_default='TRUE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=False),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner_phone_number=Column(String, ForeignKey("users.phone_number",ondelete="CASCADE"),nullable=False)
    status=Column(String,server_default='Waiting for response',nullable=False)

    owner = relationship("User", foreign_keys=[owner_id])


class User(Base):
    __tablename__ = "users"
    phone_number = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    home_location = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))

    __table_args__ = (
        CheckConstraint(
            cast(phone_number, INTEGER) > 0, #checking if the phone_number value can be cast to an integer and is greater than 0
            name='phone_number_positive_integer'
        ),
        CheckConstraint(
            text("length(phone_number) = 8"), #checking if the length of the phone_number value is equal to 8
            name='phone_number_eight_digits'
        )
    )

