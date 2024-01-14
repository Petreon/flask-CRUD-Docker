from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from os import environ

# i could create a blueprint for this but in the tutorial dont use so ok :c

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)

    def json(self):
        return {"id":self.id,"username":self.name,"email":self.email}
    
# i think i need use app.appcontext to use but i will leave now
with app.app_context():
    db.create_all()

#create a test route

@app.route("/test", methods=["GET"])
def test():
    ## dont need this make_response to return this but i will use cause im following the tutorial
    return make_response(jsonify({"message": "test route"}), 200)

@app.route("/users", methods=["POST"])
def create_user():
    try:
        error = None
        data = request.get_json()
        if "username" not in data or data["username"] is None:
            return make_response(jsonify({"message":"username not send"}),400)
        if "email" not in data or data["email"] is None:
            return make_response(jsonify({"message":"email not send"}),400)

        user = User.query.filter_by(name=data["username"]).first()
        if user:
            error = "problem"
        user = User.query.filter_by(email=data["email"]).first()
        
        #print(user)
        #app.logger.info("point accessed")
        app.logger.info(user)
        if error is None and user is None:
            new_user = User(name = data["username"], email = data["email"]) ## o error está aqui
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({"message": f"User {data['username']} created"}), 201)
        return make_response(jsonify({"message":"User already exists"}),409)

    except e: ## e is a global object for handling errors
        return make_response(jsonify({"message":"error creating an user"}), 500)
    
#get all users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all() ## get all the users from the database
        return make_response(jsonify({"users": [user.json() for user in users]}), 200) ## interesting way to do this

    except e:
        return make_response(jsonify({"message": "error getting users"}), 500)
    
#get user by id
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user =  User.query.filter_by(id=id).first()

        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        
        return make_response(jsonify({"message": f"User with id = {id} not found"}), 404)
    
    except e:
        return make_response(jsonify({"message": f"cannot query user by id = {id}"}), 500)
    
#update a user
@app.route("/users/<int:id>", methods=["POST"])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()

            if data["username"] is not None:
                user.name = data["username"]
            if data["email"] is not None:
                user.email = data["email"]
        
            db.session.commit()
            return make_response(jsonify({"message": f"User with id = {id} updated"}), 200)
        
        return make_response(jsonify({"message": "User not found"}), 404)
    
    except e:
        return make_response(jsonify({"message": "error updating user"}),500)
    
#delete a user
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "User deleted"}),200)
        return make_response(jsonify({"message": f"cannot find User with id = {id}"}), 404)

    except e:
        return make_response(jsonify({"message": "error deleting user"}),500)
