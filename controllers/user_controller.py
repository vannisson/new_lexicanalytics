from database import db
from flask import request, Blueprint
from models.user_model import User

user_blueprint = Blueprint('user_blueprint',__name__)

@user_blueprint.route("/user", methods=["GET"])
def user_list():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return users

@user_blueprint.route("/user/<string:id>", methods=["GET"])
def user_detail(id):
    user = db.get_or_404(User, id)
    return user
    
@user_blueprint.route("/user", methods=["POST"])
def user_create():
    user = User(
        name=request.form["username"],
        email=request.form["email"],
        password=request.form["password"]
    )
    db.session.add(user)
    db.session.commit()
    return user

@user_blueprint.route("/user/<string:id>", methods=["PUT"])
def user_update(id):
    user = db.get_or_404(User, id)

    db.session.delete(user)
    db.session.commit()

    new_user = User(
      id= id,
      name=request.form["username"],
      email=request.form["email"],
      password=request.form["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

@user_blueprint.route("/user/<string:id>", methods=["DELETE"])
def user_delete(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return "Done!"
