import sys
sys.path.append('./security')
from role import Role
from db import session

# get all roles
def getRoles():
    """
    Get all roles
    """
    return  session.query(Role).all()

# get role by id
def getRole(role_id):
    """
    Get role by id
    """
    return session.query(Role).get(role_id)

#get role by name
def getRoleByName(role_name):
    """
    Get role by name
    """
    return session.query(Role).filter(Role.name == role_name).first()

#add role
def addRole(role):
    """
    Add role
    """
    session.add(role)
    session.commit()
    return role

#delete role
def deleteRole(role):
    """
    Delete role
    """
    session.delete(role)
    session.commit()
    return role

#update role
def updateRole(role, new_role):
    """
    Update role
    """
    role = new_role
    session.commit()
    return role