import os
#this creates an "absolute path" for the local SQL database file. No idea what an absolute path is
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jacqueline'
    #SQLALCHEMY_DATABASE_URI = os.environ.get(DATABASE_URL) or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
