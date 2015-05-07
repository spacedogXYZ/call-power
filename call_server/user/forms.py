# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from wtforms import (HiddenField, BooleanField, TextField,
                     PasswordField, SubmitField,
                     RadioField, DateField)
from wtforms.validators import ValidationError, Required, Length, EqualTo, Email, AnyOf
from wtforms_components import PhoneNumberField
from flask_wtf.html5 import EmailField

from .models import User
from .constants import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
                        USERNAME_LEN_MIN, USERNAME_LEN_MAX,
                        USER_ROLE, USER_STATUS)


class LoginForm(Form):
    next = HiddenField()
    login = TextField(_('Username or email'), [Required()])
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    remember = BooleanField(_('Remember me'))
    submit = SubmitField(_('Sign in'))


class UserRoleForm(Form):
    next = HiddenField()
    role_code = RadioField(_("Role"), [AnyOf([str(val) for val in USER_ROLE.keys()])],
                           choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_code = RadioField(_("Status"), [AnyOf([str(val) for val in USER_STATUS.keys()])],
                             choices=[(str(val), label) for val, label in USER_STATUS.items()])
    submit = SubmitField(_('Save'))


class UserForm(Form):
    next = HiddenField()
    email = EmailField(_('Email'), [Required(), Email()],
                       description=_("What's your email address?"))
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
                             description=_('%s characters or more' % PASSWORD_LEN_MIN))
    name = TextField(_('Choose your username'), [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
                     description=_("Don't worry. you can change it later."))
    phone = PhoneNumberField(_('Phone Number'),
                             description=_("What's your phone number?"))
    submit = SubmitField(_('Save'))

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_('This username is already registered'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email is already registered'))


class RecoverPasswordForm(Form):
    email = EmailField(_('Your email'), [Email()])
    submit = SubmitField(_('Send instructions'))


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(u'Password', [Required()])
    password_confirm = PasswordField(u'Password Confirm', [EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('Save')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reauthenticate')