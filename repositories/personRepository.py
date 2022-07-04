from entities.person import Person
from db import session
from sqlalchemy import or_,and_
# get all persons
def getPersons():
    """
    Get all persons
    """
    try:
        return session.query(Person).all()
    except:
        return "invalid data"

# get person by id
def getPerson(person_id):
    """
    Get person by id
    """
    try:
        return session.query(Person).get(person_id)
    except:
        return "invalid data"

#get person by keyword
def getPersonByKeyword(keyword):
    """
    Get person by keyword
    """
    try:
        return session.query(Person).filter(or_(Person.first_name.like('%'+keyword+'%'),Person.last_name.like('%'+keyword+'%') )).all()
    except:
        return "invalid data"

#add person
def addPerson(person):
    """
    Add person
    """
    last_name = person.last_name

    try:
        session.add(person)
        session.commit()
        return getPersonByKeyword(last_name)
    except:
        session.rollback()
        return "invalid data"

#delete person
def deletePerson(person):
    """
    Delete person
    """
    try:
        person = session.query(Person).filter(Person.id == person.id).one()
        session.delete(person)
        session.commit()
        return person
    except:
        session.rollback()
        return "invalid data"

#update person
def updatePerson(person, new_person):
    """
    Update person
    """
    try:
        p = session.query(Person).filter(Person.id == person.id).one()
        if(new_person.first_name):
            if(p.first_name != new_person.first_name):
                p.first_name = new_person.first_name
        
        if(new_person.last_name):
            if(p.last_name != new_person.last_name):
                p.last_name = new_person.last_name

        if(new_person.birthday_date):
            if(p.birthday_date != new_person.birthday_date):
                p.birthday_date = new_person.birthday_date

        if(new_person.email):
            if(p.email != new_person.email):
                p.email = new_person.email

        if(new_person.phone):
            if(p.phone != new_person.phone):
                p.phone = new_person.phone
        
        if(new_person.address):
            if(p.address != new_person.address):
                p.address = new_person.address
        if(new_person.city):
            if(p.city != new_person.city):
                p.city = new_person.city
        
        if(new_person.drivers_license):
            if(p.drivers_license != new_person.drivers_license):
                p.drivers_license = new_person.drivers_license
        
        session.commit()
        return getPerson(person.id)  
    except:
        session.rollback()
        return "invalid data"