# Django test task project




This is a project for internal use. The service is created to help employees to make a decision at the lunch place.

## Features

- Creating users
- Adding restaurants
- Adding menus
- Voting for todays menu/restaurant


## Installation

This app uses additional software you should have:
- PostgresSQL



To run application on itself localy  you should clone it from repo with 

```sh
git clone github.com/Parydubets/testTask
cd .\testTask\
```
Create a virtual environment
```sh
python -m venv env
env/Scripts/activate  #(for windows)
```
For app usage you need to have PostgresSQL database running. By default the database is "restaurant_service". You can change it in configuration (ssettings.py) or set environment variables


## Populating database with data
The next step you can populate the db with dummy data, using:
```
python manage.py makemigrations app
python manage.py migrate app
python manage.py populate
```

## Running localy
To run tests localy use command: 
```sh
pytest testTask --create-db
```
To run service localy use:
```
python manage.py runserver
```

## Running with docker
To run with docker use command: 
```
docker-compose up --build
```

## API

This project have a branch of api available:
- /api/users
POST request: Creates new account
- /api/users/<int:id>
PUT request: Updates the accoun with idt


- /api/restaurants
GET request: Returns a list of restaurants
- /api/restaurants/<int:id>
POST request: Creates a new restaurant
PUT request: Updates a restaurant


- /api/menus
GET request: Returns list of restaurants` menus for current day of the week
- /api/menus/<int:id>
POST request: Adds a new menu for chosen restaurant and day
PUT request: Edits menu


- /api/votes
GET request: Returns list of votes with time
POST request: Voting for menu/restaurant
- /api/top_votes
GET request: Returns 2 best restaurants by votes


- /api/token
POST request: Returns refresh and access jwt


## All the data in requests is sent/received in JSON except menu data. Menu data create/update is using froms
