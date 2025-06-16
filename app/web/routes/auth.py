from quart import Blueprint, render_template, flash, redirect, url_for
from quart_auth import AuthUser, login_required, login_user, logout_user

from app.web.forms.login_form import LoginForm
from app.core.use_cases.auth import get_user_by_credentials

auth_bp = Blueprint(
    name="auth",
    url_prefix="/auth", 
    import_name=__name__,
    template_folder="../../templates",
    static_folder="../../static"
)

@auth_bp.route("/login", methods=["GET"])
async def render_login():
    login_form: LoginForm = await LoginForm.new()
    return await render_template("auth/login_page.html", form=login_form)


@auth_bp.route("/login", methods=["POST"])
async def login():
    login_form: LoginForm = await LoginForm.new()
    
    if await login_form.validate_on_submit():
        email: str = login_form.email.data or ""
        password: str = login_form.password.data or ""
        user = await get_user_by_credentials(email, password)

        if not user:
            await flash("Invalid credentials!")
            return redirect(url_for("auth.render_login"))

        login_user(AuthUser(user.email), remember=True)

        await flash("Login successful!")
        return redirect("/scans")
    
    await flash("Invalid credentials!")
    return redirect(url_for("auth.render_login"))


@auth_bp.route("/check_session", methods=["GET"])
@login_required
async def check_session():
    return "OK"


@auth_bp.route("/logout", methods=["GET"])
@login_required
async def logout():
    logout_user()
    await flash("Logout successful!")
    return redirect(url_for("auth.render_login"))