import jwt
from flask import request, abort, Response, json, jsonify

from src import app, db, logger
from src.models.token_store_model import TokenStore
from src.utilities.utility import generate_access_token, update_token_store


# Below function checks validity of access tokens on protected routes
# This function implements auto-renewal of access tokens
'''
@app.before_request
def check_authenticity():
    # Exclude a specific route from header check
    request.new_access_token = ''
    if '/signup' == request.path or '/authenticate' == request.path or '/refresh-access-token' == request.path or '/access-token' == request.path:
        return
    required_headers = ['Refresh-Token', 'Authorization']
    for header in required_headers:
        if header not in request.headers:
            logger.debug(f'Request does not have {header} header while accessing path {request.path}')
            abort(Response(
                status=400,
                response=json.dumps({
                    'result': "Bad request",
                    "error": f'{header} header is missing'
                }),
                mimetype='application/json'
            ))
    access_token = request.headers.get('Authorization')
    refresh_token = request.headers.get('Refresh-Token')
    token_store_item = TokenStore.query.filter(TokenStore.access_token == access_token).first()

    if token_store_item is not None:
        try:
            jwt.decode(access_token, app.config['AUTH_SECRET_KEY'], algorithms=["HS256"])
            logger.debug(
                f'While accessing path {request.path} by user {token_store_item.email} access token is valid; request to be served')
        except jwt.ExpiredSignatureError:
            logger.debug(
                f'While accessing path {request.path} by user {token_store_item.email} access token is expired, checking for refresh_token validity')
            # Check if refresh access_token is valid
            try:
                jwt.decode(refresh_token, app.config['REFRESH_SECRET_KEY'], algorithms=["HS256"])
                app.logger.debug(
                    f'While accessing path {request.path} by user {token_store_item.email} generating new access token using refresh token')
                # Generate a JWT access_token for access
                token = generate_access_token(token_store_item.email)
                request.new_access_token = token
                app.logger.debug(
                    f'While accessing path {request.path} by user {token_store_item.email} updating access token in the store')
                # update access token in the store
                update_token_store(request.headers.get('Authorization'), request.new_access_token)

            except jwt.ExpiredSignatureError:
                app.logger.debug(
                    f'While accessing path {request.path} by user {token_store_item.email}, both tokens are expired; request aborted')
                abort(Response(
                    response=json.dumps({
                        'result': "Authentication access_token and refresh_token expired",
                        "error": "Both access access_token and refresh tokens are expired. Use /authenticate to "
                                 "obtain new tokens"}),
                    status=401,
                    mimetype='application/json'
                ))
            except jwt.InvalidTokenError:
                app.logger.debug(
                    f'While accessing path {request.path} by user {token_store_item.email} refresh token in invalid, deleting the token from store; request aborted')
                # Delete the invalid token from store
                db.session.delete(token_store_item)
                db.session.commit()
                abort(Response(
                    response=json.dumps({
                        'result': "Authentication access_token and refresh tokens invalid",
                        "error": "Both access access_token and refresh tokens are expired or invalid. Use /authenticate to "
                                 "obtain new tokens"}),
                    status=401,
                    mimetype='application/json'
                ))
        except jwt.InvalidTokenError:
            app.logger.debug(
                f'While accessing path {request.path} by user {token_store_item.email} access token in invalid, deleting the token from store; request aborted')
            # Delete the invalid token from store
            db.session.delete(token_store_item)
            db.session.commit()
            abort(Response(
                response=json.dumps({
                    'result': "Invalid access_token",
                    "error": "Authentication access_token is invalid. Use /authenticate to obtain a valid auth access access_token"}),
                status=401,
                mimetype='application/json'
            ))
    else:
        logger.debug(
            f'While accessing path {request.path}, token not found in the store; request aborted')
        abort(Response(
            response=json.dumps({
                'result': "Request not authenticated",
                "error": "Authentication access_token is either expired or invalid. Use /authenticate to obtain a valid auth "
                         "access access_token"}),
            status=401,
            mimetype='application/json'
        ))
'''


# Below function checks validity of access tokens on protected routes
@app.before_request
def check_authenticity():
    # Exclude a specific route from header check
    request.new_access_token = ''
    if '/signup' == request.path or '/authenticate' == request.path or '/refresh-access-token' == request.path or '/access-token' == request.path:
        return
    required_headers = ['Authorization']
    for header in required_headers:
        if header not in request.headers:
            logger.debug(f'Request does not have {header} header while accessing path {request.path}')
            abort(Response(
                status=400,
                response=json.dumps({
                    'result': "Bad request",
                    "error": f'{header} header is missing'
                }),
                mimetype='application/json'
            ))
    access_token = request.headers.get('Authorization')
    token_store_item = TokenStore.query.filter(TokenStore.access_token == access_token).first()

    if token_store_item is not None:
        try:
            jwt.decode(access_token, app.config['AUTH_SECRET_KEY'], algorithms=["HS256"])
            logger.debug(
                f'While accessing path {request.path} by user {token_store_item.email} access token is valid; request to be served')

        except jwt.ExpiredSignatureError:
            app.logger.debug(
                f'While accessing path {request.path} by user {token_store_item.email}, access token is expired; request aborted')
            abort(Response(
                response=json.dumps({
                    'result': "Authentication access_token expired",
                    "error": "Access_token is expired. Use /refresh-access-token to "
                             "obtain new access tokens"}),
                status=401,
                mimetype='application/json'
            ))
        except jwt.InvalidTokenError:
            app.logger.debug(
                f'While accessing path {request.path} by user {token_store_item.email} access token in invalid, deleting the token from store; request aborted')
            # Delete the invalid token from store
            db.session.delete(token_store_item)
            db.session.commit()
            abort(Response(
                response=json.dumps({
                    'result': "Invalid access_token",
                    "error": "Authentication access_token is invalid. Use /authenticate to obtain a valid auth access access_token"}),
                status=401,
                mimetype='application/json'
        ))
    else:
        logger.debug(
            f'While accessing path {request.path}, token not found in the store; request aborted')
        abort(Response(
            response=json.dumps({
                'result': "Request not authenticated",
                "error": "Authentication access_token is either expired or invalid. Use /authenticate to obtain a valid auth "
                         "access access_token"}),
            status=401,
            mimetype='application/json'
        ))



@app.after_request
def inject_new_access_token(response):
    if not request.new_access_token == '':
        logger.debug(f'Injecting a new access token in the response')
        token = {
            'access_token': request.new_access_token,
        }
        response_data = response.get_json()
        # Add the additional data to the response data
        if response_data:
            response_data.update(token)
        else:
            response_data = token
        # Update the response with the modified data
        response.set_data(jsonify(response_data).data)
    return response
