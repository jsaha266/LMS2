from flask_security import Security, SQLAlchemySessionUserDatastore, hash_password
from applications.model import User, Role
from applications.database import db

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)