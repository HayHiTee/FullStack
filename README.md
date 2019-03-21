# FullStack Shopping Cart

This project is a challenge to test my full stack skills for Turing Remote Company 

## Getting Started

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes. See deployment for notes
on how to deploy the project on a live system

## Prerequisites
* Python version 3.6 or 3.7 
* Django 2.1 
* Optional - > Pycharm or robust IDE

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

1. clone this repository.

2. create a virtual environment with python 3.6 or 3.7 for the project
    * Click [here](https://docs.python.org/3/library/venv.html) to learn how to 
    create virtual environment for python project

3. Run the following command to install the packages in the requirements.

```bash
pip install -r requirements.txt
``` 
 or in case you are not using virtual environment and have multiple python versions installed.
```bash
pip3 install -r requirements.txt
```

* Once the requirements are installed, cd into the project directory where 'manage.py' resides.

* See Usage
 

# Usage

Add or make changes to 'CashCard/settings.py' with the following if they are not already included.

Configure and choose Database type- Default is Sqlite.

For help on Database, check Django documentation [here](https://docs.djangoproject.com/en/2.1/topics/install/#database-installation)

```python
import  os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Use this for authentication(App is using abstract User)
AUTH_USER_MODEL = 'FullStackApp.User'

#Add list of host(s) here - required for production
ALLOWED_HOSTS = []

# Add the following installed apps here in settings if not included
INSTALLED_APPS = [
    # ...
    'FullStackApp.apps.FullstackappConfig',
    'django.contrib.admin',
    # ...
]

# Add Database here
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


TEMPLATES = [
    {
       # ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        # ...
    },
]

STATIC_URL = '/static/'

# Where collectstatic will store all the collected static files
# You must create the directory in the root folder
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'Media')

CART_SESSION_ID = 'cart'


```
* Set environment variables for Secret Key - Ask For Secret Key

* Once settings configuration is completed, make and create migrations for database.

* Run the following commands

Make migrations
```bash
python manage.py makemigrations

```

Migrate with this command
```bash
python manage.py migrate

```

Start the server

If 'My Port' is not included, server starts at 8000

```bash
python manage.py runserver 'My Port'

```

## Production
Check out [deploying django to heroku](https://devcenter.heroku.com/articles/django-app-configuration) 

* Add the following to settings

```python
#This on top
import django_heroku

# Should be at the bottoom
django_heroku.settings(locals())
```

* Create 'runtime.txt' in the root repository and add the following
```bash
python-3.7.1
```

* Create 'Procfile' file in the root repository and add the following
```bash
release: python manage.py migrate

web: gunicorn FullStackApp.wsgi --log-file -

```

## Contributing
Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
All properties belong to [Hayhitee](https://hayhitee.herokuapp.com)
