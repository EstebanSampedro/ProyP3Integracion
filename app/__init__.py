# __init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'una_clave_secreta_muy_segura'
    
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
