class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KET = 'mysecretkey'
    BASIC_AUTH_FORCE = True