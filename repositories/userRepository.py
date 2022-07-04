from repositories.roleRepository import getRoleByName
from repositories.vehicleRepository import getVehicleByPlateNumber
from security.user import User
from security.Auth import AuthHandler
from db import session


auth = AuthHandler()

# get all users
def getUsers():
    """
    Get all users
    """
    try:
        return session.query(User.id,User.username, User.role_id).all()
    except:
        return "invalid data"
# get user by id
def getUser(user_id):
    """
    Get user by id
    """
    try:
        return session.query(User.id,User.username, User.role_id).filter(User.id == user_id).first()
    except:
        return "invalid data"


# get user by username
def getUserByUsername(username):
    """
    Get user by username
    """
    try:
        return session.query(User).filter(User.username == username).first()
    except:
        return "invalid data"


#get user by his vehicle
def getUserByVehicle(vehicle):
    try:
        return session.query(User.id,User.username, User.role_id).filter(User.id == vehicle.person_id).first()
    except:
        return "invalid data"

#get user by keyword
def getUserByKeyword(keyword):
    try:
        return session.query(User.id,User.username, User.role_id).filter(User.username.like('%'+keyword+'%')).all()
    except:
        return "invalid data"

# add user
def addUser(user):
    """
    Add user
    """
    try:
        session.add(user)
        session.commit()
        return user
    except:
        session.rollback()
        return "invalid data"

# delete user
def deleteUser(userid):
    """
    Delete user
    """
    try:
        user =  session.query(User).filter(User.id == userid).one()
        session.delete(user)
        session.commit()
        return user 
    except:
        session.rollback()
        return "invalid data"
#change password
def changePassword(user):
    """
    Change password
    """
    try:
        up_user = session.query(User).filter(User.id == user.id).one()
        up_user.password = user.password
        session.commit()
        return user
    except:
        session.rollback()
        return "invalid data"

#is an admin
def isAdmin(user):
    try:
        role = getRoleByName("admin")
        if(session.query(User).filter_by(role_id=role.id,username = user.username).first()):
            return True
        return False
    except:
        return "invalid data"

#verify token
def verifyToken(token):
    try:
        if(token):
            userId = auth.decode_token(token)
            user = getUser(userId)
            if user:
                return True
            return False
        return False
    except:
        session.rollback()
        return "invalid data"

#verify token and admin role
def verifyTokenAndAdmin(token):
    try:
        if(token):
            userId = auth.decode_token(token)
            if userId == "Signature has expired":
                return False
            if userId == "Invalid token":
                return False
            user = getUser(userId)
            if user and isAdmin(user):
                return True
            return False
        return False
    except:
        session.rollback()
        return "invalid data"