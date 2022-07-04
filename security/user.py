
from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50))
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey("roles.id"))

    def __repr__(self):
        return "<User(username='%s', role_id='%s')>" % (self.username, self.role_id)