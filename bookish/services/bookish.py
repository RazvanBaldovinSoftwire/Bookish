from operator import itemgetter

from flask import request

from bookish.models.book import Book
from bookish.models import db, book
from bookish.models.borrows import Borrows
from bookish.models.user import User
import jwt
from datetime import datetime, timedelta
from bookish.services.error_handler import *


def get_table(database):
    try:
        return database.query.all()
    except Exception as e:
        return e


def get_every(table):
    return [line.serialize() for line in table]


def verify_token(user_token):
    try:
        user_id = jwt.decode(user_token, "secret", algorithms=["HS256"])
    except:
        raise BadToken()
    return user_id["id"]


def add_user(user_data):
    user = User.query.filter_by(name=user_data["name"], password=user_data["password"]).first()
    if user:
        raise Conflict()

    new_user = User(name=user_data['name'], password=user_data['password'], token="0")

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        raise InternalServerError()

    raise Created("user")


def login_user(user_login):
    user = User.query.filter_by(name=user_login["name"], password=user_login["password"]).first()

    try:
        user.token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
        db.session.commit()
        return {"message": "User has logged in successfully. Generated token: {}".format(user.token)}
    except:
        raise NotFound("User")


def logout_user(user_token):
    user_id = verify_token(user_token)

    user = User.query.filter_by(id=user_id).first()
    try:
        user.token = 0
        db.session.commit()
        return {"message": "User has logged out successfully."}
    except:
        raise NotFound("User")


def delete_user(user_token):
    user_id = verify_token(user_token)

    user = User.query.filter_by(id=user_id).first()
    borrowed_books = Borrows.filter_by(id_user=user_id).all()
    if not borrowed_books:
        raise MethodNotAllowed()

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User has logged out successfully (for a very long time :D)."}
    except:
        raise NotFound("User")


def add_book(book_add):
    new_book = Book(isbn=book_add['isbn'], title=book_add['title'], author=book_add['author'],
                    copies=book_add['copies'], available=book_add['copies'])

    try:
        db.session.add(new_book)
        db.session.commit()
        raise Created("book")
    except:
        raise InternalServerError()


def delete_book(book_delete):
    book = Book.query.filter_by(isbn=book_delete['isbn']).first()

    if book.available != book.copies:
        return {"error": "Book cannot be deleted. The books are still borrowed."}

    try:
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book has been deleted successfully."}
    except:
        raise NotFound("Book with given ISBN")


def borrow_book(book_borrowe, user_token):
    user_id = verify_token(user_token)

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        raise NotFound("User")

    book = Book.query.filter_by(isbn=book_borrowe['isbn']).first()
    if book and book.available > 0:
        borrowed = Borrows(user.id, isbn=book_borrowe["isbn"],
                           return_date=datetime.now() + timedelta(days=book_borrowe["days"]))
        try:
            db.session.add(borrowed)
            book.available -= 1
            db.session.commit()
            return {"message": "Book borrowed successfully."}
        except:
            raise InternalServerError()

    raise NotFound("Book with given ISBN")


def get_user_borrows(user_token):
    user_id = verify_token(user_token)

    borrowed_books = Borrows.query.filter_by(id_user=user_id).all()
    return get_every(borrowed_books)

def return_book(book_returne, user_token):
    user_id = verify_token(user_token)

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        raise NotFound("User")

    book = Book.query.filter_by(isbn=book_returne['isbn']).first()
    book_borrowed = Borrows.query.filter_by(isbn=book_returne['isbn'], id_user=user_id).first()
    if book and book_borrowed:
        try:
            db.session.delete(book_borrowed)
            book.available += 1
            db.session.commit()
            return {"message": "Book returned successfully."}
        except:
            raise InternalServerError()

    raise NotFound("Book with given ISBN")


def search_book(book_searche, books):
    if "title" in book_searche:
        books = [book for book in books if book.title == book_searche["title"]]
    if "author" in book_searche:
        books = [book for book in books if book.author == book_searche["author"]]
    return get_every(books)


def get_params():
    param_order = request.args.get("order")
    param_limit = request.args.get("limit")

    params = {"order": param_order if param_order else "ASC",
              "limit": int(param_limit) if (param_limit and param_limit.isnumeric()) else -1}

    return params


def format_books_output(books, params):
    if params["order"] == "ASC":
        output = sorted(books, key=itemgetter("Title"))
    elif params["order"] == "DESC":
        output = sorted(books, key=itemgetter("Title"), reverse=True)
    else:
        raise BadRequest()

    if params["limit"] != -1:
        return output[:params["limit"]]
    return output
