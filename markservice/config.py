from dotenv import load_dotenv
from authx import AuthX, AuthXConfig
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS") 
DB_PORT = os.getenv("DB_PORT") 

RABBIT_CONN = os.getenv("RABBIT_CONN") 


config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "user_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
config.JWT_ACCESS_TOKEN_EXPIRES = 300

security = AuthX(config=config)