class Dev:
    MONGO_URI = "mongodb://127.0.0.1:27017/pyfly"

class Prod:
    pass

config = {
        "Dev": Dev,
        "Prod": Prod
        }


