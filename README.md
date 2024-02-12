# Authenticate Service

Implementation of an Auth REST API service in Python

## Table of Contents

- [About](#about)
- [Installation](#Installation)
- [Features](#features)
- [Further Improvements](#further-improvements)


## About

The purpose of this project is to provide an implementation of an Auth REST API service in Python

## Installation
### Prerequisites 
- Docker

### Installation 

- Clone the repository
``` 
git clone https://github.com/saxenankit123/auth-service.git
```
- Change directory to `auth-service`
```
cd auth-service
```
- Give execute permission to the `install.sh` file and run it. This command will build the docker image of auth-service and run it. Once done, you would be able to run the curl commands mentioned in the features section.
```
chmod +x install.sh
./install.sh
```
Once successful, the `install.sh` script will print the container id for stopping or starting the service later.

- To stop or re-run the auth-service use below commands

```
docker stop YOUR_AUTH-SERVICE_CONTAINER_ID
docker start YOUR_AUTH-SERVICE_CONTAINER_ID

```

## Features

- ### Sign up 
creation of user using email and password - A new user can signup by providing a valid email id and password. Email id should be unique and password must be atleast **6 characters** long.

```curl
curl -i --location --request POST 'http://localhost:3000/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "ankit@gmail.com",
    "password": "Ind1a@765"
}'
```
Sample Response
 ```
{
    "result": "Account successfully created"
}
```
Response HTTP Codes

| HTTP Status Code | Description                                                           |
|-----------------|-----------------------------------------------------------------------|
| 400             | Request validation fails; signup unsuccessful                                              |
| 409             | Record with the provided email id already exists; signup unsuccessful |
 | 201             | User signup successful                                                |

---

- ### Sign in
once an account is created, using email and password, client can obtain `access_token` and `refresh_token` to access protected routes.
```curl
curl -i --location --request GET 'http://localhost:3000/authenticate' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "ankit@gmail.com",
    "password": "Ind1a@765"
}'
```
Sample Response
 ```
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "result": "Authentication successful"
}

```
`access_token` - Authentication token that should be used in every subsequent request to access protected routes. **acces_stoken has an expiry of 1 minute.**

`refresh_token` - Token to be used to renew `access_token`. **refresh_token has an expiry of 2 mins.**

*How to renew access token ?* - while accessing a protected route, client should first check if the `access_token` is expired. If yes, then client should initiate call to `/refresh-access-token` route to receive new `access_token`. If `refresh_token` is also expired then client should use `/authenticate` to receive new `access_token` and `refresh_token` by passing valid email and password.

Response HTTP Codes

| HTTP Status Code | Description                                          |
|------------------|------------------------------------------------------|
| 400              | Request validation fails                             |
| 401              | Incorrect email id or password; sign in unsuccessful |
 | 200              | User signin successful                               |

---
- ### Fetch user profile
a protected route to fetch user profile details. You need to pass a valid `access_token` to access this route.
```curl
curl -i --location --request GET 'http://localhost:3000/user' \
--header 'Content-Type: application/json' \
--header 'Authorization: YOUR_ACCESS_TOKEN' \
--data-raw '{
    "email": "EMAIL_ADDRESS_OF_USER"
}'
```
Sample Response
 ```
{
    "data": {
        "email": "EMAIL_ADDRESS_OF_USER"
    },
    "result": "User profile fetched successfully",
    "status": 200
}
```
Response HTTP Codes

| HTTP Status Code | Description                                   |
|------------------|-----------------------------------------------|
| 400              | Request validation fails |
| 404              | User not found                                |
| 200              | User profile fetch successful                 |
|401|Authentication failed| 
---
- ### Refresh access token
if `access_token` is expired then client can call this route to refresh the `access_token` by passing a valid `refresh_token`
```curl
curl -i --location --request GET 'http://localhost:3000/refresh-access-token' \
--header 'Content-Type: application/json' \
--data '{
    "refresh_token":"YOUR_REFRESH_TOKEN"
}'
```
Sample Response
 ```
{
    "access_token": "NEW_ACCESS_TOKEN",
    "result": "Access token refreshed successful"
}
```
Response HTTP Codes

| HTTP Status Code | Description                                               |
|------------------|-----------------------------------------------------------|
| 400              | Request validation fails                                  |
| 404              | Token not present; refresh unsuccessful                   |
| 200              | Access token refresh successful                           |
|401| Refresh token is expired or invalid; refresh unsuccessful | 
---
- ### Remove access token
to remove `access_token` forcibly

**CAUTION** - Preferred secured approach should be to create a simple shell script that can run on the backend server. This script can take takes emailid as input argument and can connect to the token store (database in the current implementation) and delete the token from token store. In the current implementation, an API is exposed to remove the token.

```curl
curl -i --location --request DELETE 'http://localhost:3000/access-token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"EMAIL_ADDRESS_OF_USER"
}'
```
Sample Response
 ```
{
    "result": "Access token removed"
}
```
Response HTTP Codes

| HTTP Status Code | Description                                               |
|------------------|-----------------------------------------------------------|
| 400              | Request validation fails                                  |
| 404              | Token not present; remove unsuccessful                    |
| 200              | Access token removed                            |
---

## Further Improvements
1. Customize the validation messages:  auth-service uses python library `jsonschema` to validate request payload/parameters. As a further improvement, it can be explored to customize the default validation messages for easy understanding.
2. In current implementation .env is present on the git repo. A safe and secure way should be to store the .env file on the server OR pull the .env file from a service.
3. In current implementation, database is being accessed from the controller layer. It can be discussed to create service and database layers to make the code more modular.
3. Make a shell script to delete the tokens from backend
4. Another way to renew `access_token` be auto-renewal. `auth_service` can auto-renew the `access_token` if the client also sends `refresh_token` in every subsequent call to access protected routes. Method `check_authenticity()` in `middleware.py` implements this but is commented in the current version.