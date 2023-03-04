from app.controller.api import ListAPI, ListsAPI, CardAPI, CardsAPI, UserAPI, AuthAPI, SummaryAPI, ExportAPI, ExportByListAPI
from flask import Flask
from flask_restful import Api
from app.config import LocalDevelopmentConfig
from app.data.database import db
from app.jobs import workers
from app.data.cache import cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.jobs import tasks

app = None
api = None
celery = None


def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app)

    app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()

    JWTManager(app)
    app.app_context().push()

    db.init_app(app)
    app.app_context().push()

    api = Api(app)
    app.app_context().push()

    # Create celery
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone='Asia/Calcutta',
        enable_utc=False
    )

    celery.Task = workers.ContextTask
    app.app_context().push()

    cache.init_app(app)
    app.app_context().push()

    print("App setup complete")
    return app, api, celery


app, api, celery = create_app()


api.add_resource(UserAPI, '/api/user/register', '/api/user/logout')
api.add_resource(AuthAPI, '/api/user/login')
api.add_resource(ListAPI, '/api/list', '/api/list/<int:id>')
api.add_resource(CardAPI, '/api/card', '/api/card/<int:id>',
                 '/api/card/<int:card_id>/<int:list_id>')
api.add_resource(ListsAPI, '/api/lists')
api.add_resource(CardsAPI, '/api/cards')
api.add_resource(SummaryAPI, '/api/user/summary')
api.add_resource(ExportAPI, '/api/export', '/api/import')
api.add_resource(ExportByListAPI, '/api/export/<int:id>')


if __name__ == '__main__':
    # Run the Flask app
    app.run()
