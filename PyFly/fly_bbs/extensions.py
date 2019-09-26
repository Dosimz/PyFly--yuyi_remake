from flask_pymongo import PyMongo
# import pymongo

mongo = PyMongo()

def init_extensions(app):

    mongo.init_app(app)

