## Ecommerce REST API
---
### __Postman collection__

[Collection](https://documenter.getpostman.com/view/16061399/Tzm8Gvw1#cbd307a3-475d-48c2-ab7e-b51ad5c8b6ea)
### __Deployed to Heroku__

[Ecommerce REST API](https://still-sea-87640.herokuapp.com/)

### __Getting started__

These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes. 

---

#### __Prerequisites__

 This is a project written using Python, Django, and Django Rest Framework

#### __1. Clone the repository__
```
$ git clone https://github.com/BolotZhusupekov07/scaling-parakeet
```
#### __2. Generate a new secret key__
You can use [ Djecrety](https://djecrety.ir/) to quickly generate
 secure secret keys.   
#### __3. Create a new PostgreSQL database__

Assuming you already have pgAdmin and postgres installed.

In your terminal:
```
$ psql postgres
$ CREATE DATABASE databasename
$ \connect databasename
```
Go into pgAdmin, login, and check that the new database exists on the dbserver.
The database credentials to go in your project’s settings.py are the same credentials for pgAdmin.
##### *setting.py*
```
DATABASES = {
             ‘default’: {
                 ‘ENGINE’: ‘django.db.backends.postgresql_psycopg2’,
                 ‘NAME’: env(‘DATABASE_NAME’),
                 ‘USER’: env(‘DATABASE_USER’),
                 'HOST': env('DATABASE_HOST),
                 ‘PASSWORD’: env(‘DATABASE_PASS’),
                 'PORT': env('DATABASE_PORT')
       }
 }

```                                                                                       
                                                               
#### __4. Build the Docker Image__
In your terminal:

```
$ docker-compose build 
```
#### __5. Create a new superuser__
```
$ docker-compose run --rm app_name python manage.py createsuperuser
```
#### __6.Run the project__
Start the development server and ensure everything is running without errors.
```
$ docker-compose up
```

#### __7.Running tests__
---
You can run the automated tests for this project with
```
$ docker-compose run --rm app_name python manage.py test
```
#### __Built With__
---
`Django` - The framework used  
`Django Rest Framework` - The toolkit used to build API  
`API Blueprint` - for API documentation



