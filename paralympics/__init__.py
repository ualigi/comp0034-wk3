import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow


# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/
class Base(DeclarativeBase):
    pass


# First create the db object using the SQLAlchemy constructor.
# Pass a subclass of either DeclarativeBase or DeclarativeBaseNoMeta to the constructor.
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # Generate your own SECRET_KEY using python secrets
        SECRET_KEY='l-tirPCf1S44mWAGoWqWlA',
        # configure the SQLite database, relative to the app instance folder
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'paralympics.sqlite'),
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise Flask with the SQLAlchemy database extension
    db.init_app(app)

    ma.init_app(app)

    # Models are defined in the models module, so you must import them before calling create_all, otherwise SQLAlchemy
    # will not know about them.
    # Create the tables in the database
    # create_all does not update tables if they are already in the database.
    with app.app_context():
        
        #from paralympics import User, Region, Event

        # Create the database and tables if they don't already exist
        db.create_all()

        # Add the data to the database if not already added
        from paralympics.database_utils import add_data
        add_data(db)

        # Register the routes with the app in the context
        from paralympics import paralympics

    return app


# Import can be here instead (but not at the top of the file) to avoid circular import issues
from paralympics.models import Region, Event, User