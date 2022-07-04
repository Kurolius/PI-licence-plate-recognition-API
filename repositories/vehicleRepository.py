from entities.vehicle import Vehicle
from db import session

#get all vehicles
def getVehicles():
    """
    Get all vehicles
    """
    try:
        return session.query(Vehicle).all()
    except:
        return "invalid data"
#get vehicle by id
def getVehicle(vehicle_id):
    """
    Get vehicle by id
    """
    try:
        return session.query(Vehicle).get(vehicle_id)
    except:
        return "invalid data"
#get vehicle by owner
def getVehicleByOwner(owner_id):
    """
    Get vehicle by owner
    """
    try:
        return session.query(Vehicle).filter(Vehicle.person_id == owner_id).all()
    except:
        return "invalid data"
#get vehicle by plate number
def getVehicleByPlateNumber(plate_number):
    """
    Get vehicle by plate number
    """
    try:
        return session.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()
    except:
        return "invalid data"


#get vehicle by keyword
def getVehicleByKeyword(keyword):
    """
    Get vehicle by keyword
    """
    try:
        return session.query(Vehicle).filter(Vehicle.model.like('%'+keyword+'%')).all()
    except:
        return "invalid data"

#add vehicle
def addVehicle(vehicle):
    """
    Add vehicle
    """
    try:
        session.add(vehicle)
        session.commit()
        return getVehicleByKeyword(vehicle.model)
    except:
        session.rollback()
        return "invalid data"

#delete vehicle
def deleteVehicle(vehicleData):
    """
    Delete vehicle
    """
    try:
        vehicle = session.query(Vehicle).filter(Vehicle.id == vehicleData.id).one()
        session.delete(vehicle)
        session.commit()
        return vehicle
    except:
        session.rollback()
        return "invalid data"

#update vehicle
def updateVehicle(new_vehicle):
    """
    Update vehicle
    """
    try:
        vehicle = session.query(Vehicle).filter(Vehicle.id == new_vehicle.id).one()
        if(new_vehicle.brand):
            if(vehicle.brand != new_vehicle.brand):
                vehicle.brand = new_vehicle.brand
        
        if(new_vehicle.model):
            if(vehicle.model != new_vehicle.model):
                vehicle.model = new_vehicle.model
        
        if(new_vehicle.year):
            if(vehicle.year != new_vehicle.year):
                vehicle.year = new_vehicle.year

        if(new_vehicle.plate_number):
            if(vehicle.plate_number != new_vehicle.plate_number):
                vehicle.plate_number = new_vehicle.plate_number

        if(new_vehicle.person_id):
            if(vehicle.person_id != new_vehicle.person_id):
                vehicle.person_id = new_vehicle.person_id
            
            
        session.commit()
        return getVehicle(vehicle.id)
    except:
        session.rollback()
        return "invalid data"