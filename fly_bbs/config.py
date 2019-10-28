class Dev:
    MONGO_URI = "mongodb://127.0.0.1:27017/pyfly"

    WTF_CSRF_ENABLED = False

class Prod:
    pass

config = {
        "Dev": Dev,
        "Prod": Prod
        }


