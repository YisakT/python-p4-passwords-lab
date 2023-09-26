

from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204

class Signup(Resource):
    def post(self):
        try:
            json = request.get_json()
            user = User(username=json['username'])
            user.password_hash = json['password']
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return {"username": user.username, "id": user.id}, 201
        except Exception as e:
            return {"error": str(e)}, 500

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {}, 204
        
        user = db.session.get(User, user_id)
        if not user:
            return {}, 204

        return user.to_dict(), 200

class Login(Resource):
    def post(self):
        json = request.get_json()
        user = User.query.filter_by(username=json['username']).first()

        if user and user.authenticate(json['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {"message": "Invalid credentials"}, 401

class Logout(Resource):
    def delete(self):
        session['user_id'] = None  
        return {}, 204

api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
