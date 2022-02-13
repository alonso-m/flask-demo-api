class DevConfig():        
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    JWT_SECRET_KEY="secretkey"
    PROPAGATE_EXCEPTIONS = True