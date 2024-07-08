from flask import request

from bookish.models.book import Book
from bookish.models.example import Example
from bookish.models import db, book
from bookish.models.user import User


def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/example', methods=['POST', 'GET'])
    def handle_example():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_example = Example(data1=data['data1'], data2=data['data2'])
                db.session.add(new_example)
                db.session.commit()
                return {"message": "New example has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            examples = Example.query.all()
            results = [
                {
                    'id': example.id,
                    'data1': example.data1,
                    'data2': example.data2
                } for example in examples]
            return {"examples": results}

    @app.route('/get_users', methods=['GET'])
    def handle_get_users():
        users = User.query.all()
        results = [
            {
                'id': user.id,
                'name': user.name,
                'password': user.password
            } for user in users]
        return {"users": results}

    @app.route('/signup', methods=['POST'])
    def handle_signup():
        if request.is_json:
            data = request.get_json()
            new_user = User(name=data['name'], password=data['password'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": "New user has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    # TEMPORARY (FIXME: introduce cookies)
    @app.route('/login', methods=['POST'])
    def handle_login():
        if request.is_json:
            user_login = request.get_json()
            users = User.query.all()
            results = [
                {
                    'id': user.id,
                    'name': user.name,
                    'password': user.password
                } for user in users if user.name == user_login['name'] and user.password == user_login['password']]
            return {"message": "New user has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/add_book', methods=['POST'])
    def handle_add_book():
        if request.is_json:
            data = request.get_json()
            new_book = Book(isbn=data['isbn'], title=data['title'], author=data['author'], copies=data['copies'],
                            available=data['available'])
            db.session.add(new_book)
            db.session.commit()
            return {"message": "New book has been added successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/get_books', methods=['GET'])
    def handle_get_books():
        books = Book.query.all()
        results = [
            {
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'copies': book.copies,
                'available': book.available
            } for book in books]
        return {"books": results}

    @app.route('/delete_book', methods=['DELETE'])
    def handle_delete_book():
        books = Book.query.all()
        data = request.get_json()

        for book in books:
            if book.isbn == data['isbn']:
                db.session.delete(book)
                db.session.commit()
                return {"message": "Book has been deleted successfully."}

        return {"message": "Book with given ISBN is not in the library"}

# 9786060868040 - Fram