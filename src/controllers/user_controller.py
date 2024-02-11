from flask import request, Response, json, jsonify
from jsonschema import validate, FormatChecker
from src import db, app
from src.models.user_model import User


def fetch_profile():
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
        app.logger.error(f'Error occurred while validating fetching profile for a user', str(e))
        return jsonify({
            'result': 'Error occurred',
            'error': str(e)
        }), 400
    email = data.get('email')
    user_profile = db.session.query(User).filter(User.email==email).first()
    if user_profile is None:
        app.logger.debug(f'No user found with email address - {email}')
        return Response(
            response=json.dumps({
                'result': "User not found",
            }),
            mimetype='application/json',
            status=404
        )
    else:
        app.logger.debug(f'Profile fetched successfully for user with email address - {email}')
        return Response(
            response=json.dumps({
                'result': "User profile fetched successfully",
                'status': 200,
                'data':{
                    'email':user_profile.email
                },
            }),
            mimetype='application/json',
            status=200
        )
