from flask import jsonify, request
from src import app
from src.controllers import auth_controller, user_controller
from src.controllers.auth_controller import remove_access_token, refresh_access_token


# POST request for signup
@app.route('/signup', methods=['POST'])
def signup():
    return auth_controller.create_user()


# GET request to authenticate
@app.route('/authenticate', methods=['GET'])
def authenticate():
    return auth_controller.authenticate()


# GET request to fetch user profile
@app.route('/user', methods=['GET'])
def fetch_profile():
    return user_controller.fetch_profile()

# GET request to obtain a new access token from refresh token
@app.route('/refresh-access-token',methods=['GET'])
def refresh_token():
    return refresh_access_token()

@app.route('/access-token',methods=['DELETE'])
def remove_token():
    return remove_access_token()