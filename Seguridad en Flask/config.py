class Config:
    SECRET_KEY = "dhdehdhe82hdueh"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:admin123@localhost/app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False