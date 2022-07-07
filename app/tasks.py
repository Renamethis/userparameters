from .extensions import celery, db
from .models import User, Parameter
import os

# Celery users managing tasks
@celery.task
def add_user_task(username):
    user = User.query.get(username)
    if(user is None):
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return user.to_json()
    return None

@celery.task
def get_users_task():
    users = [u.to_json() for u in User.query.all()]
    return users

@celery.task
def delete_user_task(username):
    user = User.query.get(username)
    if(user is None):
        return None
    db.session.delete(user)
    for param in Parameter.query.filter_by(username=username):
        db.session.delete(param)
    db.session.commit()
    return user.to_json()

# Celery parameters managing tasks
@celery.task
def get_parameters_task(username):
    user = User.query.get(username)
    if(user is None):
        return None
    parameters = [param.to_json() for param in \
        Parameter.query.filter_by(username=username)]
    return parameters

@celery.task
def get_parameter_task(username, name, type):
    user = User.query.get(username)
    if(user is None):
        return None
    parameter = Parameter.query.get((username, name, type))
    if(parameter is None):
        return None
    return parameter.to_json()

@celery.task
def set_parameter_task(username, name, type, value):
    user = User.query.get(username)
    if(user is None):
        return 404
    parameter = Parameter.query.get((username, name, type))
    if(type == 'int' and not value.isdigit()):
        return 400
    if(parameter is None):
        parameter = Parameter(
            username=username,
            parameterName=name,
            ptype=type,
            value=value
        )
        db.session.add(parameter)
        db.session.commit()
    else:
        parameter.value = value
        db.session.commit()
    return 200
