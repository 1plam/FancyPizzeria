import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'src', 'sessions')
    SESSION_PERMANENT = False

    # Optional: Uncomment the line below to set the session file directory on macOS
    # SESSION_FILE_DIR = '/Users/<username>/tempdir'
