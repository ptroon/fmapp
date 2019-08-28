from project import db, bcrypt
from project.models import User, Role
from sqlalchemy import exc

db.create_all()
try:
    print ("trying to execute")
    #res = User.query.filter_by(login_id='philip').first()
    #user = User('bob', 'Philip', 'Troon', 'User account for Philip', 'password', 'philip@somewhere.com', 1)
    #db.session.delete(res)
    #db.session.commit()
    #print ("deleted user " + res.forename)
    #res = User.query.filter_by(login_id='bob').first()
    #print ("Found {} {}".format(res.forename,res.surname))
    user2 = User('philip', 'Philip', 'Troon', 'User account for Philip Troon', 'test', 'philip@somewhere.com', 2)
    user3 = User('bob', 'Bob', 'Smith', 'User account for Bob Smith', 'test', 'bob@somewhere.com', 1)
    user4 = User('frank', 'Frank', 'Green', 'User account for Frank Green', 'test', 'frank@somewhere.com', 1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)

    #role1 = Role("Standard User Access", 0, "CHANGES")
    #role2 = Role("Administrator User Access", 1, "CHANGES,ADMIN")
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.commit()
except:
    print("Unexpected error:", sys.exc_info()[0])
db.session.rollback()
