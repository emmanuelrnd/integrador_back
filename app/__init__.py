from flask import Flask
from flask_cors import CORS
from config import Config

from .routes.user_bp import film_bp

from .database import DatabaseConnection
from .models.exceptions import FilmNotFound,InvalidDataError

def init_app():

    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    CORS(app, supports_credentials=True)

    app.config.from_object(
        Config
    )

    DatabaseConnection.set_config(app.config)
    
    @app.errorhandler(FilmNotFound)
    def handle_film_not_found_error(error):
        return error.get_response()
    
    @app.errorhandler(InvalidDataError)
    def handle_ivalid_data_error(error):
        return error.get_response()
    
    app.register_blueprint(film_bp, url_prefix = '/films')

    return app