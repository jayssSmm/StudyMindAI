from flask import Flask
from app.routes.main import bp as main_bp
from app.routes.prompt import bp as prompt_bp
from app.routes.uploads import bp as upload_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "ss@//42"

    app.register_blueprint(main_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(upload_bp)

    return app