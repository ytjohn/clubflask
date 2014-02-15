from flask_wtf import Form
from wtforms import TextField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User, Profile


class RegisterForm(Form):
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                    validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                                validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False

        self.user = user
        return True


class ProfileForm(Form):
    first_name = TextField('First Name', validators=[DataRequired()])
    last_name = TextField('Last Name', validators=[DataRequired()])
    callsign  = TextField('Call Sign', validators=[Length(min=3, max=8)])


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.callsign = None

    def validate(self):
        initial_validation = super(ProfileForm, self).validate()
        if not initial_validation:
            return False
        callsign = Profile.query.filter_by(callsign=self.callsign.data).first()
        if callsign:
            self.callsign.errors.append("Callsign already registered by someone else? Could it be another you?")
            return False
 
        self.callsign = callsign
        return True