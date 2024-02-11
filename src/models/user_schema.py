user_schema = {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email"
            },
            "password": {
                "type": "string",
                "minLength": 6,
            }
        },
        "required": ["email", "password"]
}

user_auth_schema = {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
            },
            "password": {
                "type": "string",
            }
        },
        "required": ["email", "password"]
    }