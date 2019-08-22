from project import db, bcrypt
from project.models import User

user = User('philip', 'Philip', 'Troon', 'password', 'philip@somewhere.com', 1)
db.session.add(user)
db.session.commit()
