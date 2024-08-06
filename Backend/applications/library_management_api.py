from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request as req
from flask_security import auth_token_required, roles_required, roles_accepted, current_user
from applications.model import *
from applications.marshal_fields import *
from datetime import datetime

# For the store management API, we will have the following endpoints:
# 1. GET /api/v1/get_all_sections - Get all sections
# 2. GET /api/v1/section/<section_id> - Get a section
# 3. POST /api/v1/section - Add a section
# 4. PUT /api/v1/section/<section_id> - Update a section
# 5. DELETE /api/v1/section/<section_id> - Delete a section
# 6. GET /api/v1/books/<section_id> - Get all books in a section
# 7. GET /api/v1/book/<book_id> - Get a book
# 8. POST /api/v1/book - Add a book
# 9. PUT /api/v1/book/<book_id> - Update a book
# 10. DELETE /api/v1/book/<book_id> - Delete a book




class AllSections(Resource):  
    @marshal_with(section)
    def get(self):
        sections = Section.query.all()
        return sections


class BooksAPI(Resource):
    def get(self, section_id):
        section = Section.query.get(section_id)
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        
        books = Book.query.filter_by(section_id=section_id).all()
        response = []
        for book in books:
            response.append({
                'book_id':book.id,
                'title':book.title,
                'content_type':book.content_type,
                'content':book.content,
                'author':book.author,
                'image':book.image,
                'date_created':datetime.strftime(book.date_created,'%Y-%m-%d'),
                'download_price':book.download_price,
                'section_id':book.section_id
            })

        return make_response(jsonify(response),200)
    

class Books(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        
        section = Section.query.get(book.section_id)
        response = {
            'book_id':book.id,
            'title':book.title,
            'content_type':book.content_type,
            'content':book.content,
            'author':book.author,
            'image':book.image,
            'date_created':datetime.strftime(book.date_created,'%Y-%m-%d'),
            'download_price':book.download_price,
            'section':{
                'section_id':section.id,
                'name':section.name,
                'description':section.description
            }
        }
        return make_response(jsonify(response),200)
    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = req.get_json()

        title = data.get('title')
        content_type = data.get('content_type')
        content = data.get('content')
        author = data.get('author')
        image = data.get('image')
        download_price = float(data.get('download_price'))
        section_id = int(data.get('section_id'))
        

        if not title or not content_type or not content or not author or not download_price or not section_id:
            return make_response(jsonify({'message':'All fields are required'}),400)
        
        section = Section.query.get(section_id)
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        
        try:
            book = Book(title=title,content_type=content_type,content=content,author=author,image=image,download_price=download_price,section_id=section_id,date_created=datetime.now())
            db.session.add(book)
            db.session.commit()
            response = {
                'message':'Book added successfully',
                'book':{
                    'book_id':book.id,
                    'title':book.title,
                    'content_type':book.content_type,
                    'content':book.content,
                    'author':book.author,
                    'image':book.image,
                    'date_created':datetime.strftime(book.date_created,'%Y-%m-%d'),
                    'download_price':book.download_price,
                    'section_id':book.section_id
                }
            }
            return make_response(jsonify(response),201)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('admin')
    def put(self,id):
        book = Book.query.get(id)
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        
        data = req.get_json()

        title = data.get('title')
        content_type = data.get('content_type')
        content = data.get('content')
        author = data.get('author')
        image = data.get('image')
        download_price = float(data.get('download_price'))
        section_id = int(data.get('section_id'))

        if not title and not content_type and not content and not author and not download_price and not section_id:
            return make_response(jsonify({'message':'Edit request is empty with any data'}),400)
        
        if title:
            book.title = title
        if content_type:
            book.content_type = content_type
        if content:
            book.content = content
        if author:
            book.author = author
        if image:
            book.image = image
        if download_price:
            book.download_price = download_price
        if section_id:
            section = Section.query.get(section_id)
            if not section:
                return make_response(jsonify({'message':'Section does not exist'}),404)
            book.section_id = section_id
        
        try:
            db.session.commit()
            return make_response(jsonify({'message':'Book updated successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('admin')
    def delete(self,id):
        book = Book.query.get(id)
        if not book:
            return make_response(jsonify({'message':'Book does not exist'}),404)
        
        try:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message':'Book deleted successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

class Sections(Resource):
    @marshal_with(section)
    def get(self,id):
        section = Section.query.get(id)
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        return section
    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = req.get_json()

        name = data.get('name')
        description = data.get('description')
        image = data.get('image')

        if not name or not description:
            return make_response(jsonify({'message':'Name and Description are required'}),400)
        
        try:
            section = Section(name=name,description=description,image=image,date_created=datetime.now())
            db.session.add(section)
            db.session.commit()
            response = {
                'message':'Section added successfully',
                'section':{
                    'section_id':section.id,
                    'name':section.name,
                    'description':section.description,
                    'image':section.image,
                    'date_created':datetime.strftime(section.date_created,'%Y-%m-%d') 
                }
            }
            return make_response(jsonify(response),201)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        

    @auth_token_required
    @roles_required('admin')
    def put(self,id):
        section = Section.query.get(id)
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        
        data = req.get_json()

        name = data.get('name')
        description = data.get('description')
        image = data.get('image')

        if not name and not description and not image:
            return make_response(jsonify({'message':'Edit request is empty with any data'}),400)
        
        if name and Section.query.filter_by(name=name).first():
            return make_response(jsonify({'message':'Section already exists'}),400)
        
        if name:
            section.name = name
        if description:
            section.description = description
        if image:
            section.image = image
        
        try:
            db.session.commit()
            return make_response(jsonify({'message':'Section updated successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('admin')
    def delete(self,id):
        section = Section.query.get(id)
        if not section:
            return make_response(jsonify({'message':'Section does not exist'}),404)
        
        try:
            db.session.delete(section)
            db.session.commit()
            return make_response(jsonify({'message':'Section deleted successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)