from project import db, bcrypt
from project.models import User
from sqlalchemy import exc

db.create_all()
try:
    print ("trying to execute")
    #user = User('bob', 'Philip', 'Troon', 'User account for Philip', 'password', 'philip@somewhere.com', 1)
    #db.session.add(user)

    res = User.query.filter_by(login_id='bob').first()
    print ("Found {} {}".format(res.forename,res.surname))

    user2 = User('bob', 'Bob', 'Smith', 'User account for Bob Smith', 'test123', 'bob@somewhere.com', 1)
    db.session.add(user2)
    db.session.commit()
except exc.IntegrityError as e:
    print("Error: with login - not unique ")
db.session.rollback()
