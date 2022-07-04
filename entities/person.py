
from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db import Base

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    birthday_date = Column(DateTime)
    email = Column(String(50))
    phone = Column(String(20))
    address = Column(String(255))
    city = Column(String(255))
    drivers_license = Column(String(20))
    vehicle = relationship("Vehicle")
    
    def __repr__(self):
        return "<Person(first_name='%s', last_name='%s', birthday_date='%s',email='%s', phone='%s', address='%s', city='%s', drivers_license='%s')>" % (
                                self.first_name, self.last_name, self.birthday_date, self.email, self.phone, self.address, self.city, self.drivers_license)