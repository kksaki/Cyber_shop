# BigBasket Shopping Website

SunJiaqi


## Website link

https://shrouded-everglades-97784.herokuapp.com/

## Prepared Data

[BIGBASKET PRODUCT | CHINMAY SHANBHAG ](https://www.kaggle.com/datasets/chinmayshanbhag/big-basket-products) by Kaggle

<<<<<<< HEAD
⚠️ There is a slight difference between codio and github commits, due to the different settings required for localhost, celery and rabbitmq to run locally and on codio


=======
>>>>>>> 037cab08645c1a08835fcf3aba7cec4c5024590c
## Starting Server

Create `.env` file in root directory with below contents.

⚠️ DO NOT commit `.env` file into this repository.

```.env
DEBUG=True
```
Then, start the server with this command.

```commandline
# install dependencies
pip install -r requirements.txt

# create database
python3 manage.py parse_csv

# run server
python3 manage.py runserver 8000

# run server in Codio
python3 manage.py runserver 0.0.0.0:8000
```

## Running Tests

```commandline
python3 manage.py test
```

## Running Behave Tests

```commandline
behave
```

## When Updated models

```commandline
# create files for migration
python3 manage.py makemigrations

# execute migration
python3 manage.py migrate
```

## For Deployment in Heroku, render

```commandline
# create requirements.txt
pip list --format=freeze > requirements.txt
<<<<<<< HEAD
```
=======
```
>>>>>>> 037cab08645c1a08835fcf3aba7cec4c5024590c
