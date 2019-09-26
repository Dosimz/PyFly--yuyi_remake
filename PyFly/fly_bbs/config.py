
class Dev:
    MONGO_URI = "mongodb://localhost:27017/PyFlyDatabase"

class Prod:
    pass

config = {
    "Dev": Dev,
    "Prod": Prod
        }
