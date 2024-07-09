from flask import request

from bookish.models.book import Book
from bookish.models import db, book
from bookish.models.borrows import Borrows
from bookish.models.user import User
import jwt
from datetime import datetime, timedelta


def get_every(table):
    return [line.serialize() for line in table]


def verify_token(user_token):
    try:
        user_id = jwt.decode(user_token, "secret", algorithms=["HS256"])
    except Exception as e:
        return {"error": str(e)}
    return user_id["id"]


def add_user(user_data):
    user = User.query.filter_by(name=user_data["name"], password=user_data["password"]).first()
    if user:
        return {"error": "User already exists"}

    try:
        new_user = User(name=user_data['name'], password=user_data['password'], token="0")
    except Exception as e:
        return {"error": str(e)}

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return {"error": str(e)}

    return {"message": "New user has been created successfully."}


def login_user(user_login):
    user = User.query.filter_by(name=user_login["name"], password=user_login["password"]).first()

    try:
        user.token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
        db.session.commit()
        return {"message": "User has logged in successfully. Generated token: {}".format(user.token)}
    except:
        return {"error": "User doesn't exist. Try signing up."}


def logout_user(user_token):
    user_id = verify_token(user_token)
    if type(user_id) is not int:
        return user_id

    user = User.query.filter_by(id=user_id).first()
    try:
        user.token = 0
        db.session.commit()
        return {"message": "User has logged out successfully."}
    except:
        return {"error": "User doesn't exist. Try logging in."}


def delete_user(user_token):
    user_id = verify_token(user_token)
    if type(user_id) is not int:
        return user_id

    user = User.query.filter_by(id=user_id).first()

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User has logged out successfully (for a very long time :D)."}
    except:
        return {"error": "User doesn't exist. Try signing up."}


def add_book(book_added):
    try:
        new_book = Book(isbn=book_added['isbn'], title=book_added['title'], author=book_added['author'],
                        copies=book_added['copies'], available=book_added['copies'])
    except Exception as e:
        return {"error": str(e)}

    try:
        db.session.add(new_book)
        db.session.commit()
        return {"message": "New book has been added successfully."}
    except Exception as e:
        return {"error": str(e)}


def delete_book(book_deleted):
    book = Book.query.filter_by(isbn=book_deleted['isbn']).first()

    if book.available != book.copies:
        return {"error": "Book cannot be deleted. The books are still borrowed."}

    try:
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book has been deleted successfully."}
    except:
        return {"error": "Book with given ISBN is not in the library"}


def borrow_book(book_borrowed, user_token):
    user_id = verify_token(user_token)
    if type(user_id) is not int:
        return user_id

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return {"error": "User doesn't exist or isn't logged in."}

    book = Book.query.filter_by(isbn=book_borrowed['isbn']).first()
    print(book)
    if book and book.available > 0:
        borrowed = Borrows(user.id, isbn=book_borrowed["isbn"],
                           return_date=datetime.now() + timedelta(days=book_borrowed["days"]))
        try:
            db.session.add(borrowed)
            book.available -= 1
            db.session.commit()
            return {"message": "Book borrowed successfully."}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Book with given ISBN is not in the library"}


def get_user_borrows(user_token):
    user_id = verify_token(user_token)
    if type(user_id) is not int:
        return user_id

    borrowed_books = Borrows.query.filter_by(id_user=user_id).all()
    return get_every(borrowed_books)

def return_book(book_returned, user_token):
    user_id = verify_token(user_token)
    if type(user_id) is not int:
        return user_id

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return {"error": "User doesn't exist or isn't logged in."}
    print(user)

    book = Book.query.filter_by(isbn=book_returned['isbn']).first()
    book_borrowed = Borrows.query.filter_by(isbn=book_returned['isbn'], id_user=user_id).first()
    print(book)
    print(book_borrowed)
    if book and book_borrowed:
        book.available += 1
        try:
            db.session.delete(book_borrowed)
            db.session.commit()
            return {"message": "Book returned successfully."}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Book with given ISBN is not in the library"}


def search_book(book_searched, books):
    if "title" in book_searched:
        books = [book for book in books if book.title == book_searched["title"]]
    if "author" in book_searched:
        books = [book for book in books if book.author == book_searched["author"]]
    return get_every(books)


