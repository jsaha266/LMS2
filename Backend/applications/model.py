from applications.database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    username = db.Column(db.String(30),primary_key=True)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    # address = db.Column(db.String(100),nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255),unique=True)
    active = db.Column(db.Boolean())


    #Relationships
    roles = db.relationship('Role',secondary='role_user',backref=db.backref('users',lazy=True))

    def __repr__(self): 
        return f'<User {self.username}>' 
    
class Role(db.Model, RoleMixin):
    role_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(100),nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'

class RoleUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),db.ForeignKey('user.username'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.role_id'))

class Section(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.Date,nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True,
                      default='https://images.unsplash.com/photo-1603058817990-2b9a9abbce86?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8Ym9va3N8fHx8fHwxNzEyMzc5MTU0&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=1600')    

    #Relationships
    books = db.relationship('Book', backref='section', lazy=True)

    def __repr__(self):
        return f'<Section {self.name}>'
    

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True, default='https://images.unsplash.com/photo-1622006816342-36fe7754b0c9?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
    date_created = db.Column(db.Date, nullable=False)
    download_price = db.Column(db.Float, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    # Relationships
    requests = db.relationship('UserRequest', backref='book', lazy=True)
    ratings = db.relationship('Rating', backref='book', lazy=True)


    def __repr__(self):
        return f'<Book {self.title}>'
    
# class Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     feedback = db.Column(db.Text, nullable=True)

#     user = db.relationship('User', backref='ratings', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    username = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)  # Updated line
    rating = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref='ratings', lazy=True)


user_book = db.Table('user_book',
                     db.Column('username', db.String(30), db.ForeignKey('user.username'), primary_key=True),
                     db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
                     )


class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    user = db.relationship('User', backref='requests', lazy=True)

    def __repr__(self):
        return f'<UserRequest {self.id}>'