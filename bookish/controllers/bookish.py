from flask import request

from bookish.models.book import Book
from bookish.models.example import Example
from bookish.models import db, book
from bookish.models.user import User
import jwt
from bookish.services.bookish import *

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

    def get_database(database):
        try:
            return database.query.all()
        except Exception as e:
            return e

    @app.route('/get_users', methods=['GET'])
    def handle_get_users():
        users = get_database(User)

        if type(users) is Exception:
            return {"error": users}
        return {"users": get_users(users)}

    @app.route('/signup', methods=['POST'])
    def handle_signup():
        if request.is_json:
            data = request.get_json()
            return add_user(data)
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/login', methods=['POST'])
    def handle_login():
        if request.is_json:
            user_login = request.get_json()
            users = get_database(User)

            if type(users) is Exception:
                return {"error": users}
            return login_user(user_login, users)
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/logout', methods=['POST'])
    def handle_logout():
        if request.is_json:
            user_logout = request.get_json()
            users = get_database(User)

            if type(users) is Exception:
                return {"error": users}
            return logout_user(user_logout, users)

    @app.route('/delete_user', methods=['DELETE'])
    def handle_delete_user():
        if request.is_json:
            user_delete = request.get_json()
            users = get_database(User)

            if type(users) is Exception:
                return {"error": users}
            return delete_user(user_delete, users)

    @app.route('/add_book', methods=['POST'])
    def handle_add_book():
        if request.is_json:
            book_added = request.get_json()
            return add_book(book_added)
        else:
            return {"error": "The request payload is not in JSON format"}

    @app.route('/get_books', methods=['GET'])
    def handle_get_books():
        books = get_database(Book)

        if type(books) is Exception:
            return {"error": books}

        return {"books": get_books(books)}

    @app.route('/delete_book', methods=['DELETE'])
    def handle_delete_book():
        book_deleted = request.get_json()
        books = get_database(Book)

        if type(books) is Exception:
            return {"error": books}

        return delete_book(book_deleted, books)

    @app.route('/borrow_book', methods=['POST'])
    def handle_borrow_book():
        if request.is_json:
            book_borrowed = request.get_json()
            books = get_database(Book)
            users = get_database(User)

            if type(books) is Exception:
                return {"error": books}
            if type(users) is Exception:
                return {"error": users}

            return borrow_book(book_borrowed, books, users)
        else:
            return {"error": "The request payload is not in JSON format"}
