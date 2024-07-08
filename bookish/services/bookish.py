from flask import request

from bookish.models.book import Book
from bookish.models import db, book
from bookish.models.borrows import Borrows
from bookish.models.user import User
import jwt
from datetime import datetime, timedelta, date


def get_users(users):
    return [
        {
            'id': user.id,
            'name': user.name,
            'password': user.password,
            'token': user.token
        } for user in users]


def add_user(data):
    try:
        new_user = User(name=data['name'], password=data['password'], token="0")
    except Exception as e:
        return {"error": e}

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return {"error": e}

    return {"message": "New user has been created successfully."}


def login_user(user_login, users):
    for user in users:
        if user_login['name'] == user.name and user_login['password'] == user.password:
            user.token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
            db.session.commit()
            return {"message": "User has logged in successfully. Generated token: {}".format(user.token)}
    return {"error": "User doesn't exist. Try signing up."}


def logout_user(user_logout, users):
    user_id = jwt.decode(user_logout['token'], "secret", algorithms=["HS256"])
    for user in users:
        if user_id["id"] == user.id:
            user.token = 0
            db.session.commit()
            return {"message": "User has logged out successfully."}

    return {"error": "User doesn't exist. Try logging in."}


def delete_user(user_delete, users):
    user_id = jwt.decode(user_delete['token'], "secret", algorithms=["HS256"])
    for user in users:
        if user_id["id"] == user.id:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User has logged out successfully (for a very long time :D)."}

    return {"error": "User doesn't exist. Try signing up."}

def add_book(book_added):
    try:
        new_book = Book(isbn=book_added['isbn'], title=book_added['title'], author=book_added['author'],
                        copies=book_added['copies'], available=book_added['available'])
    except Exception as e:
        return {"error": e}

    try:
        db.session.add(new_book)
        db.session.commit()
        return {"message": "New book has been added successfully."}
    except Exception as e:
        return {"error": e}


def get_books(books):
    return [
        {
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'copies': book.copies,
            'available': book.available
        } for book in books]


def delete_book(book_deleted, books):
    for book in books:
        if book.isbn == book_deleted['isbn']:
            try:
                db.session.delete(book)
                db.session.commit()
                return {"message": "Book has been deleted successfully."}
            except Exception as e:
                return {"error": e}

    return {"error": "Book with given ISBN is not in the library"}


def borrow_book(book_borrowed, books, users):
    user_id = jwt.decode(book_borrowed["token"], "secret", algorithms=["HS256"])
    for book in books:
        if book.isbn == book_borrowed["isbn"] and book.available > 0:
            for user in users:
                if user_id["id"] == user.id:
                    borrowed = Borrows(user_id, isbn=book_borrowed["isbn"],
                                       return_date=book_borrowed["return_date"])
                    try:
                        db.session.add(borrowed)
                        db.session.commit()
                        book.available -= 1
                        db.session.commit()
                        return {"message": "Book borrowed successfully."}
                    except Exception as e:
                        return {"error": str(e)}
            return {"error": "User nor found."}

    return {"error": "Book with given ISBN is not in the library"}
