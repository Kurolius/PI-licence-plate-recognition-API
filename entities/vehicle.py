
from sqlalchemy import Sequence
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, Sequence('vehicle_id_seq'), primary_key=True)
    brand = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    plate_number = Column(String(20))
    person_id = Column(Integer, ForeignKey("persons.id"))

    def __repr__(self):
        return "<Vehicle(brand='%s', model='%s', image='%s', plate_number='%s')>" % (
                                 self.brand, self.model, self.image, self.plate_number)