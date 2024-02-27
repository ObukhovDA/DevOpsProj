import os
SECRET_KEY = '1233242'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:devops@mysql_db:3306/devops'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')


