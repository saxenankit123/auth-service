from src import db, bcrypt, app, logger
from src.models.token_store_model import TokenStore
from src.models.user_model import User
from flask import request, jsonify, abort
from jsonschema import validate, FormatChecker
from src.models.user_schema import user_auth_schema, user_schema
from src.utilities.utility import generate_access_token, generate_refresh_token, is_access_token_valid, \
    is_refresh_token_valid


# Function to create a new user
def create_user():
    data = {}
    try:
        data = request.json
        validate(instance=data, schema=user_schema, format_checker=FormatChecker())
    except Exception as e:
        app.logger.error(f'Error occurred while validating signup request for a user',str(e))
        return jsonify({
            'result': 'Error occurred',
            'error': str(e)
        }), 400
    email = data.get('email')
    hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    user = db.session.query(User).filter(User.email == email).first()

    if user is not None:
        app.logger.debug(f'User already exists with email - {email}; not creating a new user')
        return jsonify({
            'result': 'Error occurred',
            'error': 'Duplicate record exists with the same email id'
        }), 409
    else:
        user_obj = User(
            email=email,
            password=hashed_password
        )
        db.session.add(user_obj)
        db.session.commit()
        db.session.close()
        return jsonify({
            'result': "Account successfully created"
        }), 201

def authenticate():
    data = {}
    try:
        data = request.json
        validate(instance=data, schema=user_auth_schema, format_checker=FormatChecker())
    except Exception as e:
        logger.error("Error occurred while validating signup request for a user", exc_info=True)
        return jsonify({
            'result': 'Error occurred',
            'error': str(e)
        }), 400
    email = data.get('email')
    password = data.get('password')
    user = db.session.query(User).filter(User.email == email).first()

    if user is None:
        logger.debug(f'No user found with email address - {email}')
        return jsonify({
            'result': 'Error occurred',
            'error': "Authentication failed - incorrect email or password"
        }), 401
    else:
        if bcrypt.check_password_hash(user.password, password):
            existing_token = TokenStore.query.filter(TokenStore.email == email).first()
            if existing_token is not None:
                if is_access_token_valid(existing_token.access_token) == 1:
                    logger.debug(f'Existing token in store is valid, returning the same for user - {email}')
                    # Return the existing token item from store
                    return jsonify({
                    'result': 'Authentication successful',
                    'access_token': existing_token.access_token,
                    'refresh_token': existing_token.refresh_token
                    }), 200
                elif is_refresh_token_valid(existing_token.refresh_token) == 1:
                    logger.debug(f'Existing token in store is expired, returing a new access token using refresh token for user - {email}')
                    # Generate JWT access_token for access
                    token = generate_access_token(email)

                    #Update the access token in the token store
                    existing_token.access_token = token
                    db.session.commit()

                    return jsonify({
                        'result': 'Authentication successful',
                        'access_token': token,
                        'refresh_token': existing_token.refresh_token
                    }), 200
                else:
                    logger.debug(f'Existing both tokens in store are expired generating new for user - {email}')
                    # Since this token is expired (both access and refresh), delete it from token store and continue with generation of new tokesn
                    db.session.delete(existing_token)
                    db.session.commit()
            else:
                logger.debug(f'No tokens present in the token store, generating new tokens for user - {email}')

            # Generate JWT access_token for access
            token = generate_access_token(email)
            # Generate refresh access_token
            refresh_token = generate_refresh_token(email)
            token_store_item = TokenStore(
                access_token=token,
                refresh_token=refresh_token,
                email=email
            )
            db.session.add(token_store_item)
            db.session.commit()

            return jsonify({
                'result': 'Authentication successful',
                'access_token': token,
                'refresh_token': refresh_token
            }), 200

        else:
            logger.debug(f'Incorrect password for user - {email}')
            return jsonify({
                'result': 'Error occurred',
                'error': "Authentication failed - incorrect email or password"
            }), 401

def refresh_access_token():
    data = {}
    try:
        data = request.json
        validate(instance=data, schema={
            "type": "object",
            "properties": {
                "refresh_token": {
                    "type": "string",
                }
            },
            "required": ["refresh_token"]
        }, format_checker=FormatChecker())
    except Exception as e:
        logger.error('Error occurred while validating refresh token request', exc_info=True)
        return jsonify({
            'result': 'Error occurred',
            'error': str(e)
        }), 400
    refresh_token = data.get('refresh_token')
    token_store_item = db.session.query(TokenStore).filter(TokenStore.refresh_token == refresh_token).first()

    if token_store_item is None:
        logger.debug(
            f'Refresh token not found in the store; request to refresh access token aborted')
        return jsonify({
            'result': 'Refresh token not found in the store; Attempt unsuccessful'
        }), 404
    else:
        if is_refresh_token_valid(refresh_token) == 1:
            logger.debug(f'Generating new access token using refresh token for user - {token_store_item.email}')
            # Generate JWT access_token for access
            token = generate_access_token(token_store_item.email)
            # Update the access token in the token store
            token_store_item.access_token = token
            db.session.commit()

            return jsonify({
                'result': 'Access token refreshed successfully',
                'access_token': token
            }), 200
        else:
            logger.debug(
                f'Refresh token is not valid or expired for user {token_store_item.email}; request to refresh access token aborted')
            return jsonify({
                'result': 'Refresh token unsuccessful',
                'error' : 'Refresh token is not valid or expired. Use /authenticate to obtain fresh tokens'

            }), 401

def remove_access_token():
    data = {}
    try:
        data = request.json
        validate(instance=data, schema={
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                }
            },
            "required": ["email"]
        }, format_checker=FormatChecker())
    except Exception as e:
        logger.error('Error occurred while attempting to remove access token', exc_info=True)
        return jsonify({
            'result': 'Error occurred',
            'error': str(e)
        }), 400
    email = data.get('email')
    token_store_item = db.session.query(TokenStore).filter(TokenStore.email == email).first()

    if token_store_item is None:
        logger.debug(f'User with email {email} not found')
        return jsonify({
            'result': 'Access token not found'
        }), 404
    else:
        db.session.delete(token_store_item)
        db.session.commit()
        logger.debug(f'Access token for user {email} successfully removed')
        return jsonify({
            'result': 'Access token removed'
        }), 200
