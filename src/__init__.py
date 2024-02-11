import os
import logging.config
from flask import Flask
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# Configure logging
# Get the directory path of the current file (__init__.py)
current_dir = os.path.dirname(__file__)

# Construct the absolute path to the configuration file
LOG_CONFIG_FILE = os.path.join(current_dir, 'config', 'logconfig.ini')
print(LOG_CONFIG_FILE)
logging.config.fileConfig(LOG_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger("file_logger")
# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app.config['AUTH_SECRET_KEY'] = os.environ.get("AUTH_SECRET_KEY")
app.config['REFRESH_SECRET_KEY'] = os.environ.get("REFRESH_SECRET_KEY")


# Initialize Bcrypt
bcrypt = Bcrypt(app)

# sql alchemy instance
db = SQLAlchemy(app)

# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)


import src.routes
import src.middlewares.middleware