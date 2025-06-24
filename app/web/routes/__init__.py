from quart import Quart, redirect, render_template, url_for
from quart_auth import Unauthorized, login_required


def add_routes(app: Quart):
    from app.web.routes.auth import auth_bp

    app.register_blueprint(auth_bp)
    
    @app.route("/", methods=["GET"])
    @login_required
    async def index():
        return await render_template("index.html")
    
    @app.route("/health", methods=["GET"])
    async def health():
        return "OK"
    
    @app.errorhandler(Unauthorized)
    async def handle_unauthorized(_):
        return redirect(url_for("auth.login"))