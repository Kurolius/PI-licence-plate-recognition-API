from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pymysql import NULL
from security.Auth import AuthHandler
from repositories.userRepository import *
from repositories.personRepository import *
from repositories.vehicleRepository import *
from repositories.roleRepository import *
from fastapi.middleware.cors import CORSMiddleware
import cv2
import plate_reco 
import numpy as np
app = FastAPI()
auth = AuthHandler()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

#----------------------------------User Routes----------------------------------------------
#get all users
@app.get("/users/")
async def get_users():
    users = getUsers()
    return  users

#get user by id
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = getUser(user_id)
    return user

#get user by keyword
@app.get("/users/keyword/{keyword}")
async def get_user_by_keyword(keyword: str):
    users = getUserByKeyword(keyword)
    return users


#Authentification
@app.post("/login")
async def login(_user : dict):
    user = getUserByUsername(_user["username"])
    if user and auth.verify_password(_user["password"], user.password):
        token = auth.encode_token(user.id)
        role = getRole(user.role_id)
        return {"token": token, "Role" : role.name}
    return {"error": "Invalid username or password"}

#create user
@app.post("/users/add")
async def add_user(_user : dict):
    if('token' in _user.keys()):
        try:
            if verifyTokenAndAdmin(_user["token"]):
                user = User()
                user.username = _user['username']
                user.password = auth.get_password_hash(_user['password'])
                role = getRoleByName(_user['role'])
                user.role_id = role.id
                return addUser(user)
            return {"error": "Invalid token"}
        except:
            return {"error": "Invalid data"}
    return {"error": "Invalid token"}

#change user password
@app.put("/users/changepassword/{user_id}")
async def update_user(user_id: int, _user : dict):
    if('token' in _user.keys()):   
        if verifyTokenAndAdmin(_user["token"]):
            olduser = getUser(user_id)
            if olduser :
                user = User()
                user.id = user_id
                user.password = auth.get_password_hash(_user['new_password'])
                return changePassword(user)
            return "Invalid username or password"
        return {"error": "Invalid token"}
    return {"error": "Invalid data"}

#delete user
@app.delete("/users/delete/")
async def delete_user( _data : dict):
    if('token' in _data.keys()):    
        if verifyTokenAndAdmin(_data["token"]):
            return deleteUser(_data["userToDelete_id"])
        return {"error": "Invalid token"}
    else:
        return {"error": "Invalid token"}
#-----------------------------------------------------------------------------------

#----------------------------------Persons Routes-----------------------------------

#get all persons
@app.get("/persons/")
async def get_persons():
    return getPersons()

#get person by id
@app.get("/persons/{person_id}")
async def get_person(person_id: int):
    return getPerson(person_id)

#get person by keyword
@app.get("/persons/keyword/{keyword}")
async def get_person_by_keyword(keyword: str):
    return getPersonByKeyword(keyword)

#create person
@app.post("/persons/add")
async def add_person(_data : dict):

    if('token' in _data.keys()):
        
        try:
            if verifyTokenAndAdmin(_data["token"]):
                person = Person()
                person.first_name = _data['first_name']
                person.last_name = _data['last_name']
                person.birthday_date = _data['birthday_date']
                person.email = _data['email']
                person.phone = _data['phone']
                person.address = _data['address']
                person.city = _data['city']
                person.drivers_license = _data['drivers_license']
                return addPerson(person)
            return {"error": "Invalid token"}
        except:
            return {"error": "Invalid data"}
    else:
        return {"error": "Invalid token"}

#upload person image
@app.post("/persons/uploadimage/{person_id}")
async def upload_person_image(token : str, person_id: int, img: UploadFile = File(...)):
    if(token == NULL):
         return "Invalid token"
    if verifyTokenAndAdmin(token):
        file_name = str(person_id)+".png"

        file_location = f"images/person/{file_name}"

        with open(file_location, "wb+") as file_object:
            file_object.write(img.file.read())
            return {"info": f"file '{file_name}' saved at '{file_location}'"}
    return {"error": "Invalid token"}

#get image
@app.get("/persons/getimage/{person_id}")
async def get_person_image(person_id: int, token : str):
    if(token == NULL):
         return "Invalid token"
    if verifyTokenAndAdmin(token):
        file_name = str(person_id)+".png"
        file_location = f"images/person/{file_name}"
        return FileResponse(file_location)
    return {"error": "Invalid token"}

#update person
@app.put("/persons/update/")
async def update_person( _data : dict):
    if verifyTokenAndAdmin(_data["token"]):
        person = Person()

        if('first_name' in _data.keys()):
            person.first_name = _data['first_name']
        if('last_name' in _data.keys()):
            person.last_name = _data['last_name']
        if('birthday_date' in _data.keys()):
            person.birthday_date = _data['birthday_date']
        if('email' in _data.keys()):
            person.email = _data['email']
        if('phone' in _data.keys()):    
            person.phone = _data['phone']
        if('address' in _data.keys()):
            person.address = _data['address']
        if('city' in _data.keys()):
            person.city = _data['city']
        if('drivers_license' in _data.keys()):
            person.drivers_license = _data['drivers_license']
        
        return updatePerson(getPerson(_data['id']), person)

    return {"error": "Invalid token"}

# delete person
@app.delete("/persons/delete/")
async def delete_person(_data : dict):
    if verifyTokenAndAdmin(_data["token"]):
        return deletePerson(getPerson(_data["person_id"]))
    return {"error": "Invalid token"}
#-----------------------------------------------------------------------------------

#----------------------------------vehicle Routes-----------------------------------

#get all vehicles
@app.get("/vehicles/")
async def get_vehicles():
    return getVehicles()

#get vehicle by id
@app.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int):
    return getVehicle(vehicle_id)

#get vehicle by keyword
@app.get("/vehicles/keyword/{keyword}")
async def get_vehicle_by_keyword(keyword: str):
    return getVehicleByKeyword(keyword)

#create vehicle 
@app.post("/vehicles/add")
async def add_vehicle(_data : dict):
    if verifyTokenAndAdmin(_data["token"]):
        vehicle = Vehicle()
        vehicle.brand = _data['brand']
        vehicle.model = _data['model']
        vehicle.year = _data['year']
        vehicle.plate_number = _data['plate_number']
        vehicle.person_id = _data['person_id']
        return addVehicle(vehicle)
    return {"error": "Invalid token"}

#upload vehicle image
@app.post("/vehicles/uploadimage/{vehicle_id}")
async def upload_vehicle_image(token : str, vehicle_id: int, img: UploadFile = File(...)):
    if verifyTokenAndAdmin(token):
        file_name = str(vehicle_id)+".png"

        file_location = f"images/vehicle/{file_name}"

        with open(file_location, "wb+") as file_object:
            file_object.write(img.file.read())
            return {"info": f"file '{file_name}' saved at '{file_location}'"}
    return {"error": "Invalid token"}

#get vehicle image
@app.get("/vehicles/getimage/{vehicle_id}")
async def get_vehicle_image(token : str, vehicle_id: int):
    if verifyTokenAndAdmin(token):
        file_name = str(vehicle_id)+".png"
        file_location = f"images/vehicle/{file_name}"
        return FileResponse(file_location)
    

#update vehicle
@app.put("/vehicles/update/")
async def update_vehicle(_data : dict):
    if verifyTokenAndAdmin(_data["token"]):
        vehicle = Vehicle()
        vehicle.id = _data["vehicle_id"]
        if('brand' in _data.keys()):
            vehicle.brand = _data['brand']
        if('model' in _data.keys()):
            vehicle.model = _data['model']
        if('year' in _data.keys()):
            vehicle.year = _data['year']
        if('plate_number' in _data.keys()):    
            vehicle.plate_number = _data['plate_number']
        if('person_id' in _data.keys()):
            vehicle.person_id = _data['person_id']
        return updateVehicle(vehicle)
    return {"error": "Invalid token"}

#delete vehicle
@app.delete("/vehicles/delete/")
async def delete_vehicle(_data : dict):
    if verifyTokenAndAdmin(_data["token"]):
        return deleteVehicle(getVehicle(_data["vehicle_id"]))
    return {"error": "Invalid token"}

#-----------------------------------------------------------------------------------

#----------------------------------Plate recognition Routes-----------------------------------

#get Vehicle by plate number
@app.get("/platerecognition/{plate_number}")
async def get_plate_recognition(plate_number: str,token : str):
    if verifyToken(token):
        return getVehicleByPlateNumber(plate_number)
    return {"error": "Invalid token"}

#get driver by Vehicle plate number
@app.get("/platerecognition/driver/{plate_number}")
async def get_plate_recognition_driver(plate_number: str,token : str):
    if verifyToken(token):
        car = getVehicleByPlateNumber(plate_number)
        if car:
            return getPerson(car.person_id)
        return {"error": "Invalid plate number"}
    return {"error": "Invalid token"}

#get person by image
@app.post("/platerecognition/person/image")
async def get_person_plate_recognition_image(token: str, file: UploadFile = File(...)):
    if verifyToken(token):
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        plate_number = plate_reco.get_license_plate(img)
        car = getVehicleByPlateNumber(plate_number)
        if car:
            return getPerson(car.person_id)
        return {"error": "Invalid plate number"}
    return {"error": "Invalid token"}

# get vehicle by image
@app.post("/platerecognition/vehicle/image")
async def get_vehicle_plate_recognition_image(token : str, file: UploadFile = File(...)):
    if verifyToken(token):
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        plate_number = plate_reco.get_license_plate(img)
        car = getVehicleByPlateNumber(plate_number)
        if car:
            return car
        return {"error": "Invalid plate number"}
        