from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "lectures"
    
    id = Column(Integer, primary_key = True, nullable = False)
    course_name = Column(String, nullable = False)
    lecture_num = Column(String, nullable = False)
    published = Column(Boolean, nullable = False, server_default = 'TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    

    owner = relationship("User")
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    full_name = Column(String, nullable=False)
    type = Column(String, nullable=False, server_default= "A")
    

class Vote(Base):
    __tablename__ = "attend"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    lec_id = Column(Integer, ForeignKey("lectures.id", ondelete="CASCADE"), primary_key=True)
