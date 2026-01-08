from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import mongo, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return "Hello World"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
