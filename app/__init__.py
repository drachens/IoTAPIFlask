from flask import Flask
from .extension import db, migrate
from .config import Config
from .routes import main_bp
from .auth import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    init_app(app) #Configura la autenticacion básica
    # Registrar Blueprints
    app.register_blueprint(main_bp)

    return app