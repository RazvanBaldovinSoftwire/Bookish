import werkzeug


class BadToken(werkzeug.exceptions.HTTPException):
    code = 498
    description = 'Invalid Token'


class Conflict(werkzeug.exceptions.HTTPException):
    code = 409
    description = 'User already exists'


class InternalServerError(werkzeug.exceptions.HTTPException):
    code = 500
    description = 'Action on database not permitted.'


class NotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Not Found'

    def __init__(self, message):
       self.description = f"{message} not found."


def not_found(message):
    return werkzeug.exceptions.NotFound(description=message)


class BadRequest(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Invalid order given'


class Created(werkzeug.exceptions.HTTPException):
    code = 201
    description = "Created"

    def __init__(self, message):
        self.description = f"New {message} added."


def created(message):
    return werkzeug.exceptions.Created(description=message)