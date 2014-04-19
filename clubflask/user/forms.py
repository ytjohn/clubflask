from flask_wtf import Form
from wtforms import TextField, PasswordField, DateField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
# from clubflask.user.models import Privacy 
#from clubflask.user.models import User, Profile, Privacy
#from clubflask.database import db    

class RegisterForm(Form):
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                    validators=[DataRequired(), Email(), Length(min=6, max=40)])
    firstname = TextField('First Name', validators=[DataRequired()])
    lastname = TextField('Last Name', validators=[DataRequired()])
    
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
    callsign  = TextField('Call Sign', validators=[Optional(), Length(min=3, max=8)])
    mobilephone = TextField('Mobile Phone', validators=[Length(max=10)])
    homephone = TextField('Home Phone', validators=[Length(max=10)])
    address = TextField(u'Mailing Address', validators=[Optional(), 
                            Length(max=200)])
    city = TextField('City')
    state = TextField('State')
    zip = TextField('Zip Code', validators=[Optional(), Length(min=5, max=5)])
    county = TextField('County')
    # These choices should come from somewhere else - the db.
    licenseclass = SelectField(u'License Class', choices=[('',''),
        ('Tech', 'Technician'), ('General', 'General'),
        ('Extra', 'Extra'), ('Novice', 'Novice'), ('Advanced', 'Advanced')], validators=[Optional()])

    # These fields are in the privacy table. Let's pull in the current record
    
    # to set defaults.
    #privacyoptions = Privacy.query.filter_by(user_id=Form.user_id).first()
    #print "prid: %s" % prid.id

    addtomailinglist = BooleanField('Add to mailing list?', default=True)
    sharewithclub = BooleanField('Share contact information with club?')
    enrollinwpaares = BooleanField('Enroll in WPA Ares?')
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.callsign = None

    def validate(self):
        initial_validation = super(ProfileForm, self).validate()
        if not initial_validation:
            return False
        return True

    
    
    