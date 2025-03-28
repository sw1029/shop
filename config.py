class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # 프로덕션에서는 True
    REMEMBER_COOKIE_HTTPONLY = True
    MAX_LOGIN_ATTEMPTS = 5
    LOGIN_LOCKOUT_TIME = 300  # seconds (5 minutes)
    USER_ACTIVITY_LOG = 'user_activity.log'