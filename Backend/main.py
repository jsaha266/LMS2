from flask import Flask

# from applications.model import User, Role
from applications.database import db
from applications.config import Config
from flask_restful import Api
from applications.user_datastore import user_datastore

from flask_security import Security, hash_password


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config) # Load configurations from Config class
    db.init_app(app) # Initialize the database

    api = Api(app, prefix='/api/v1') # Initialize the API with versioning
    
    app.security = Security(app, user_datastore) # Initialize the Flask-Security extension

    with app.app_context(): # Create all tables and roles if they don't exist
        db.create_all() 

        admin = app.security.datastore.find_or_create_role(name='admin',description='Administrator')
        # manager = app.security.datastore.find_or_create_role(name='manager',description='Manager')
        user = app.security.datastore.find_or_create_role(name='user',description = 'Customers')
        if not app.security.datastore.find_user(email="admin@gmail.com"): # Create an admin user if it doesn't exist
            app.security.datastore.create_user(email="admin@gmail.com", username='admin', password=hash_password("password"),roles = [admin])
        db.session.commit()

    return app,  api


app, api = create_app() 


from applications.auth_api import Login, Register, Logout

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(Logout,'/logout')

from applications.library_management_api import AllSections, Sections
api.add_resource(Sections,'/section','/section/<int:id>') # Add the Sections resource to the API
api.add_resource(AllSections,'/get_all_sections') # Add the AllSections resource to the API

from applications.library_management_api import Books, BooksAPI
api.add_resource(Books,'/book','/book/<int:id>') # Add the Books resource to the API
api.add_resource(BooksAPI,'/<int:section_id>/books') # Add the BooksAPI resource to the API



if __name__ == '__main__':
    app.run(debug = True)
