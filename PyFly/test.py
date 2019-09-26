from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo()
#mongo.init_app(app)

print(mongo.db.user.find_one())

if __name__ == "__main__":
    app.run()
