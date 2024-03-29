import os
from os import getenv
SECRET_KEY = getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{getenv("MYSQL_USER")}:{getenv("MYSQL_PASSWORD")}@{getenv("MYSQL_HOST")}:3306/{getenv("MYSQL_DATABASE")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')