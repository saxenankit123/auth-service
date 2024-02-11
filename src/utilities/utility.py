from datetime import datetime, timedelta
import jwt
import pytz

from src import app, db
from src.models.token_store_model import TokenStore


def generate_access_token(email):
    # Generate JWT access_token for access
    token = jwt.encode({'username': email, 'exp': datetime.now(
        pytz.timezone('Asia/Kolkata')) + timedelta(minutes=1)},
                       app.config['AUTH_SECRET_KEY'], algorithm="HS256")
    return token


def generate_refresh_token(email):
    # Generate refresh access_token
    refresh_token = jwt.encode({'username': email, 'exp': datetime.now(
        pytz.timezone('Asia/Kolkata')) + timedelta(minutes=2)},
                               app.config['REFRESH_SECRET_KEY'], algorithm="HS256")
    return refresh_token


def update_token_store(existing_token, new_access_token):
    token_store_item = TokenStore.query.filter(TokenStore.access_token == existing_token).first()
    token_store_item.access_token = new_access_token
    db.session.commit()


def is_access_token_valid(access_token):
    response = 1
    try:
        jwt.decode(access_token, app.config['AUTH_SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        response = -1
    except jwt.InvalidTokenError:
        response = -2
    return response


def is_refresh_token_valid(refresh_token):
    response = 1
    try:
        jwt.decode(refresh_token, app.config['REFRESH_SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        response = -1
    except jwt.InvalidTokenError:
        response = -2
    return response
