from flask import Flask 

from logging import Formatter, FileHandler


from .extensions import db, format_datetime
from .models import Venue, Artist, Show

from .routes.main import main

from .routes.venue import venue
from .routes.artist import artist
from .routes.show import show

from flask_migrate import Migrate
from flask_moment import Moment






def create_app(config_file='config.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)
    
    db.init_app(app)

    
    app.register_blueprint(main)
    app.register_blueprint(venue)
    app.register_blueprint(artist)
    app.register_blueprint(show)

    moment = Moment(app)
    migrate = Migrate(app,db)


    app.jinja_env.filters['datetime'] = format_datetime
    
    
    
    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    
    return app