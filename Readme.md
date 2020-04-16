# Full Stack Casting Agency API Backend

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 

## Motivation for project

This is the capstone project of Udacity fullstack nanodegree program, which demonstrate the skillset of
using Flask, SQLAlchemy, Auth0, gunicorn and heroku to develop and deploy a RESTful API. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Setting up the database

To run the tests on the api, you must add atleast 3 movies and 3 actors in the database.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the file directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python3 app.py
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `add:actors`
    - `add:movies`
    - `delete:actors`
    - `delete:movies`
    - `edit:actors`
    - `edit:movies`
    - `view:actors`
    - `view:movies`
6. Create new roles for:
    - Casting Assistant
        - Can view actors and movies`
    - Casting Director
        - All permissions a Casting Assistant has and ...
        - Add or delete an actor from the database 
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and ...
        - Add or delete a movie from the database
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Casting Assistant role to one    and Casting Director role to another, and Executive Producer   to the other.
    - Sign into each account and make note of the JWT.
    - Test each endpoint and correct any errors.

## Demo Page  

https://casting-agency001.herokuapp.com

Test each endpoint with the link above ,and different role's Jwts. 
JWTs for different role can be accessed by login to the link with username and password provided as follows.
https://dxpr.auth0.com/authorize?audience=agency&response_type=token&client_id=9Cx36gVtprw8UDjUkcHLDa11Q4jIqzeo&redirect_uri=http://localhost:8080/ 

```
- Casting Assistant
    - UserName: casting_assistant@test.com
    - Password: Udacity@1
- Casting Director
    - UserName: casting_director@test.com
    - Password: Udacity@1
- Executive Producer
    - UserName: executive_producer@test.com
    - Password: Udacity@1 
```

## Endpoints documentation

#### `GET '/movies'`
- Fetches a dictionary of movies
- Required URL Arguments: None
- Required Data Arguments: None
- Returns: Returns Json data about movies 
- Success Response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 01 Jan 2012 00:00:00 GMT",
            "title": "Lion King",
            "cast": ["Edward", "Jeff"]
        },
        {
            "id": 2,
            "release_date": "Mon, 12 Aug 2019 00:00:00 GMT",
            "title": "Joker",
            "cast": ["Jeff", "David"]
        }
    ],
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `GET '/actors'`
- Fetches a dictionary of actors
- Required Data Arguments: None
- Returns: Json data about actors
- Success Response:
```
  {
    "actors": [
        {
            "age": 36,
            "gender": "male",
            "id": 1,
            "name": "Edward",
            "movies": ["Lion King"]
        },
        {
            "age": 25,
            "gender": "other",
            "id": 2,
            "name": "David",
            "movies": ["Joker"]
        },
        {
            "age": 35,
            "gender": "female",
            "id": 3,
            "name": "Jeff",
            "movies": ["Lion King", "Joker"]
        }
    ],
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `DELETE '/movies/<int:movie_id>'`
- Deletes the `movie_id` of movie
- Required URL Arguments: `movie_id: movie_id_integer` 
- Required Data Arguments: None
- Returns: Json data about the deleted movie's ID 
- Success Response:
```
{
    "id_deleted": 5,
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `DELETE '/actors/<int:actor_id>'`
- Deletes the `actor_id` of actor
- Required URL Arguments: `actor_id: actor_id_integer` 
- Required Data Arguments: None
- Returns: Json data about the deleted actor's ID 
- Success Response:
```
{
    "id_deleted": 4,
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```


#### `POST '/movies'`
- Post a new movie in a database.
- Required URL Arguments: None 
- Required Data Arguments:  Json data                
- Success Response:
```
{
    "movie": {
        "id": 6,
        "release_date": "Thu, 01 Aug 2002 00:00:00 GMT",
        "title": "Toy Story",
        "actors": [1, 2]
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `POST '/actors'`
- Post a new actor in a database.
- Required URL Arguments: None 
- Required Data Arguments:  Json data   

- Success Response:
```
{
    "actor": {
        "age": 18,
        "gender": "other",
        "id": 4,
        "name": "Penny",
        "movies": [2, 3]
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```


#### `PATCH '/movies/<int:movie_id>'`
- Updates the `movie_id` of movie
- Required URL Arguments: `movie_id: movie_id_integer` 
- Required Data Arguments: None
- Returns: Json data about the updated movie 
- Success Response:
```
{
    "movie": {
        "id": 5,
        "release_date": "Wed, 05 Dec 2018 00:00:00 GMT",
        "title": "Avenger"
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `PATCH '/actors/<int:actor_id>'`
- Updates the `actor_id` of actor
- Required URL Arguments: `actor_id: actor_id_integer` 
- Required Data Arguments: None
- Returns: Json data about the deleted actor's ID 
- Success Response:
```
{
    "actor": {
        "age": 28,
        "gender": "other",
        "id": 4,
        "name": "Penny"
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

## Testing
For testing, required jwts are included for each role.
To run the tests, run
```
python3 test_app.py
```