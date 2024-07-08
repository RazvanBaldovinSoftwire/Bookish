from flask import request
from bookish.models.example import Example
from bookish.models import db
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

    @app.route('/user', methods=['POST', 'GET'])
    def handle_example():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_user = User(name=data['name'], password=data['password'])
                db.session.add(new_user)
                db.session.commit()
                return {"message": "New user has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            users = User.query.all()
            results = [
                {
                    'id': user.id,
                    'name': user.name,
                    'password': user.password
                } for user in users]
            return {"users": results}
