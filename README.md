# [e-inwork.com](https://e-inwork.com)
# Django User Account API
The template project for the REST API using Django

## Main Requirement
### All requirements will be automatically installed when run this application in Docker
| Name                              | Required version                                                                                                   | 
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Python                            | 3.9 or above                                                                                                              |  
| Django Framework                  | 4.1 or above                                                                                                             |
| Django REST Framework             | 3.14.0                                                                                                             |
| Django REST Framework Simple JWT  | 5.2.0                                                                                                             |
| Yet another Swagger generator     | 1.21.4                                                                                                             |
| Django CORS Header                | 3.13.0                                                                                                            |
| PostgreSQL                        | latest                                                                                                             |  

### More detail about all Python packages and requirements software for this application check on the file:
   - requirements.txt
   - docker-compose.yml

### Main Feature:
   - Custom User Model with id field using UUID
   - Login using an email
   - Base Class View REST API with a Model Serializer and a User Permission
   - JSON Web Token for the user authentication
   - CORS Allowed Host to connect with the frontend 
   - API Documentation with manual testing using Swagger
   - Unit Testing for the User REST API, including authentication login, access with a token, and update with a token 
   - Docker Compose for the development environment

## Setting up the development environment with Docker Compose
### Run the Application in the localhost environment
1. Install Docker
   - https://docs.docker.com/get-docker/
2. Git clone this repository to your localhost and from terminal run below command:
   ```
   git clone git@github.com:e-inwork-com/django-user-account-api
   ```
3. If run this application alongside the frontend at this link: https://github.com/e-inwork-com/nextjs-user-account-web-app, copy file `sample_settings.py` to `local_settings.oy` otherwise skip this step.
   ```
   cd django-user-account-api
   cd useraccountapi
   cp sample_settings.py local_settings.py
   cd ..
   cd ..
   ```
4. Change the active folder to `django-user-account-api`:
   ```
   cd django-user-account-api
   ```
5. Run Docker Composee:
   ```
   docker-compose up -d
   ```
6. Migrate DB tables for this application:
   ```
   docker-compose exec api ./manage.py migrate
   ```
7. Open the API Documentation, and manual testing on the browser:
   - http://localhost:8000

### Manual testing in the terminal using CURL
1. Create or register a user:
   ```
   curl -d '{"email":"jon@doe.com", "password":"pa55word", "first_name": "Jon", "last_name": "Doe"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/users/
   ```
2. Get a token or login :
   ```
   curl -d '{"username":"jon@doe.com", "password":"pa55word"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/token/
   ```
3. Get a current user with an access token:
   ```
   curl -H "Authorization: Bearer {access_token}" -X GET http://localhost:8000/api/users/me/
   ```
4. Update a current user with an access token :
   ```
   curl -d '{"email":"jon@email.com"}' -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" -X PATCH http://localhost:8000/api/users/me/
   ```
