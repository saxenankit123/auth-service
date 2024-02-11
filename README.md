# Authenticate Service

Implementation of an Auth REST API service in Python

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#Installation)

## About

The purpose of this project is to provide an implementation of an Auth REST API service in Python
## Features

- Sign up (creation of user) using email and password - A new user can signup by providing a valid email id and password. Email id should be unique and password must be atleast 6 characters long.

```curl
curl --location --request POST 'http://localhost:3000/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "a@a.com",
    "password": "Hello@123"
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

- Sign in
```curl
curl --location --request GET 'http://localhost:3000/authenticate' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "a@a.com",
    "password": "Hello@123"
}'
```
Sample Response
 ```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFAYS5jb20iLCJleHAiOjE3MDc2MTk4MjF9.LWTyFt88doNNB6ibHfCtJPy6M_Q313E4s9Lwqc2-Aug",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFAYS5jb20iLCJleHAiOjE3MDc2MTk4ODF9.jhd-ZHyOqQm-RVHbXjFPfcYkc6p2nNyh-ebMLQfORNQ",
  "result": "Authentication successful"
}

```
access_token - Authorization token that should be used in every subsequent request to access protected routes. This has an expiry of 1 minute
refresh_token - Token to renew access tokens. This has an expiry of 2 mins.

How to renew access token ?
1. Client initiated renewal - while accessing a protected route, client should check if the access token is expired. If yes, then client should initiate call to /refresh-access-token route to receive new access tokens
2. Another way could be auto-renewal - auth_service can auto-renew the access token if the client also sends refresh_token in every subsequent call to access protected routes. While auth-service supports this but the method check_authenticity() in middleware.py is commented. Therefore, this approach will not work


Response HTTP Codes

| HTTP Status Code | Description                                          |
|------------------|------------------------------------------------------|
| 400              | Request validation fails                             |
| 401              | Incorrect email id or password; sign in unsuccessful |
 | 200              | User signin successful                               |

---
- Fetch user profile - a protected route to fetch user profile details
```curl
curl --location --request GET 'http://localhost:3000/user' \
--header 'Content-Type: application/json' \
--header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFAYS5jb20iLCJleHAiOjE3MDc2NTI1NzZ9.752lX9PKceSPK47OPZMxxu6GSYyVVNT3i8uXZAovdF8' \
--data-raw '{
    "email": "a@a.com"
}'
```
Sample Response
 ```
{
    "data": {
        "email": "a@a.com"
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
- Refresh access token - to refresh access token by passing a valid refresh token
```curl
curl --location --request GET 'http://localhost:3000/refresh-access-token' \
--header 'Content-Type: application/json' \
--data '{
    "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFAYS5jb20iLCJleHAiOjE3MDc2NTIxMDd9.nFGGEu-lytN8aC8dy-EEgD-R9VDpCRC3qfc4_jlnkAM"
}'
```
Sample Response
 ```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFAYS5jb20iLCJleHAiOjE3MDc2NTMxMDV9.MydMs3w7h16hHVv45g614b70ry4ag7OXivuXe36o5VI",
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
- Remove access token - to remove access token forcibly from backend. 

Preferred apprach should be to create a simple script that can run on prod server, takes emailid as input and deletes the token from token store. For this implementation, exposing and API to remove the token (this should not be done on production as this is not safe/secure)

```curl
curl --location --request DELETE 'http://localhost:3000/access-token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"a@a.com"
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
## Installation
### Prerequisites 
- Docker

### Installation 

- Clone the repository
``` bash
git clone https://github.com/saxenankit123/auth-service.git
```
- Change directory to auth-service
```bash
cd auth-service
```
- Give execute permission to the start.sh file and run it
```bash
chmod +x start.sh
./start.sh
```