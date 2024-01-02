from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from google.cloud import bigquery


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    service_account_path_UK = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_UK')
    app.bigquery_client_UK = bigquery.Client.from_service_account_json(service_account_path_UK)



    from app.blueprints.data_endpoints.routes import data_blueprint
    from app.blueprints.user_endpoints.routes import user_blueprint
    app.register_blueprint(data_blueprint)  # Fix here: You've registered user_blueprint twice
    app.register_blueprint(user_blueprint)

    from app.blueprints.telamatics.routes import telamatics_blueprint
    app.register_blueprint(telamatics_blueprint)

    from app.blueprints.test.routes import test_blueprint
    app.register_blueprint(test_blueprint)

    from app.blueprints.database.routes import database_blueprint
    app.register_blueprint(database_blueprint)

    from app.blueprints.reports.routes import reports_blueprint
    app.register_blueprint(reports_blueprint)

    from app.blueprints.FFTools.routes import FFTools_blueprint
    app.register_blueprint(FFTools_blueprint)

    from app.blueprints.tools.routes import tools_blueprint
    app.register_blueprint(tools_blueprint)

    from app.blueprints.csm.routes import csm_blueprint
    app.register_blueprint(csm_blueprint)

    from app.blueprints.alerts.routes import alerts_blueprint
    app.register_blueprint(alerts_blueprint)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the base directory of your application
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Construct the absolute path for uploads folder
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app
