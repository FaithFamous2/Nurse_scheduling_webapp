from flask import Flask
from app.routes import main
import os

def create_app():
    template_dir = os.path.abspath('templates')
    static_dir = os.path.abspath('static')

    print(f"Template directory: {template_dir}")
    print(f"Static directory: {static_dir}")

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.register_blueprint(main)
    return app
