from repositories.userRepository import *
from role import Role
from repositories.roleRepository import *
from db import engine,Base,session
import sys
from security.Auth import AuthHandler
auth = AuthHandler()
sys.path.append('./')
from repositories.roleRepository import getRoles
def init_data():
    if not getRoles() :
        role = Role()
        role.name = "admin"
        role.description = "Administrator"
        session.add(role)
        session.commit()
        role = Role()
        role.name = "user"
        role.description = "General user"
        session.add(role)
        session.commit()
    if not getUsers():
        adminuser = User()
        adminuser.username = "admin"
        adminuser.password = auth.get_password_hash("admin")
        role = getRoleByName("admin")
        adminuser.role_id = role.id
        session.add(adminuser)
        session.commit()