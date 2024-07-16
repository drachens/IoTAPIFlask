from flask import Flask
from .extension import db, migrate
from .routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar Blueprints
    app.register_blueprint(main_bp)

    return app