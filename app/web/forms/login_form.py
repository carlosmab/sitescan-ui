from typing import Type

from quart_wtf import QuartForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(QuartForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


    @classmethod
    async def new(cls: Type, **kwargs) -> "LoginForm":
        return await cls.create_form(**kwargs)