
import sys
sys.path.append('./')
from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, Sequence('role_id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    user = relationship("User")

    def __repr__(self):
        return "<Role(name='%s', description='%s')>" % (self.name, self.description)
