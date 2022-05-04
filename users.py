import secrets
from db import db
from flask import session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return ['Username does not exist!']
    else:
        if check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return [f'Successfully logged in as {username}!']
        else:
            return ['Wrong password!']


def logout():
    del session["user_id"]


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (:username,:password_hash)"
        db.session.execute(
            sql, {"username": username, "password_hash": hash_value})
        db.session.commit()
    except IntegrityError:
        return ['Username taken! Please pick another username.']
    except:
        return ['An error occured, please try again later!']
    return login(username, password)


def user_id():
    return session.get("user_id", 0)

def is_user():
    return user_id() != 0

def get_username(id):
    if id == 0:
        return ""
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()[0]