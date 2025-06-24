# app/app.py
from quart import Quart
from quart_auth import QuartAuth
from app.settings import get_settings
from app.web.routes import add_routes
from dotenv import load_dotenv

load_dotenv(override=True)

def create_app() -> Quart:
    app = Quart(__name__)

    settings = get_settings()
    # Apply settings from Pydantic config
    app.secret_key = settings.SECRET_KEY
    app.config["DEBUG"] = settings.DEBUG
    app.config["WTF_CSRF_ENABLED"] = settings.WTF_CSRF_ENABLED

    add_routes(app)
    QuartAuth(app)
    
    # Register blueprints, middleware, etc.
    # from app.web.routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    return app

# Required for QUART_APP=app.app
app = create_app()
