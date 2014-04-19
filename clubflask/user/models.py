# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from clubflask.database import db, CRUDMixin
from clubflask.extensions import bcrypt


class User(UserMixin, CRUDMixin, db.Model):

    __tablename__ = 'users'
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # The hashed password
    created_at = db.Column(db.DateTime(), nullable=False)
    active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())
    is_verified = db.Column(db.Boolean())
    profile = db.relationship('Profile', backref='user',
                                lazy='dynamic')

    # these fields I want to remove, which involves dropping the entire database.
    # first_name = db.Column(db.String(30), nullable= True)
    # last_name = db.Column(db.String(30), nullable=True)

    def __init__(self, username=None, email=None, password=None,
                 active=False, is_verified=False, is_admin=False):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
        self.active = active
        self.is_admin = is_admin
        self.is_verified = is_verified
        self.created_at = dt.datetime.utcnow()


    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<User "{username}">'.format(username=self.username)


class Attributes(CRUDMixin, db.Model):
    """ This table will define attributes that can be associated with
    a user. """
    
    __tablename__ = 'attributes'
    
    shortname = db.Column(db.String(10), nullable=False, unique=True)
    description = db.Column(db.String(80), nullable=False)
    placeholder = db.Column(db.String(30), nullable=True)
        
    def __init__(self):
        """ Let's pre-load all the attributes """
    
        if not Attributes.query.filter_by(id=1).first():
            Attributes.create(id=1, shortname='firstname', 
                                description='First Name')
        if not Attributes.query.filter_by(id=2).first():
            Attributes.create(id=2, shortname='lastname', 
                                description='Last Name')   
        db.session.commit()
        
class UserAttributes(CRUDMixin, db.Model):
    """ This table will contain a list of attributes and values associated
    with a user. """
    
    __tablename__ = 'userattributes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.id'),                            nullable=False)
    value = db.Column(db.String(200), nullable=False)
    
class Profile(CRUDMixin, db.Model):

    __tablename__ = 'profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    # Contact Information
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    mobilephone = db.Column(db.String(20), nullable=True)
    homephone = db.Column(db.String(20), nullable=True)
    callsign = db.Column(db.String(10), unique=True, nullable=True)
    licenseclass = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(80), unique=False, nullable=True)
    city = db.Column(db.String(80), unique=False, nullable=True)
    state = db.Column(db.String(80), unique=False, nullable=True)
    zip = db.Column(db.String(11), unique=False, nullable=True)
    county = db.Column(db.String(30), nullable=True)


    privacy = db.relationship('Privacy', backref='profile',
                                lazy='dynamic')
    usercapabilities = db.relationship('UserCapabilities', backref='profile',
                                lazy='dynamic')

    def __init__(self, user_id=None, first_name=None, last_name=None):
        self.user_id = user_id  
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)




class Privacy(UserMixin, CRUDMixin, db.Model):

    __tablename__ = 'privacy'

    # Privacy
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    addtomailinglist = db.Column(db.Boolean())
    sharewithclub = db.Column(db.Boolean())
    enrollinwpaares = db.Column(db.Boolean())


class UserCapabilities(CRUDMixin, db.Model):

    __tablename__ = 'usercapabilities'
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    capability_id = db.Column(db.Integer, db.ForeignKey('capabilities.id'))
    value = db.Column(db.Boolean())


class Capabilities(UserMixin, CRUDMixin, db.Model):


    # Capabilities
    __tablename__ = 'capabilities'
    name = db.Column(db.String(30), unique=True, nullable=False)
    wpaname = db.Column(db.String(30), unique=True)
    wpavalue = db.Column(db.String(30))

#     emergencypower = db.Column(db.Boolean())
#
#     # bands to operate on
#     ssb_hf = db.Column(db.Boolean())
#     ssb_6m = db.Column(db.Boolean())
#     ssb_2m = db.Column(db.Boolean())
#     ssb_220 = db.Column(db.Boolean())
#     ssb_440 = db.Column(db.Boolean())
#     cw_hf = db.Column(db.Boolean())
#     cw_6m = db.Column(db.Boolean())
#     cw_2m = db.Column(db.Boolean())
#     cw_220 = db.Column(db.Boolean())
#     cw_440 = db.Column(db.Boolean())
#     fm_hf = db.Column(db.Boolean())
#     fm_6m = db.Column(db.Boolean())
#     fm_2m = db.Column(db.Boolean())
#     fm_220 = db.Column(db.Boolean())
#     fm_440 = db.Column(db.Boolean())
#     data_hf = db.Column(db.Boolean())
#     data_6m = db.Column(db.Boolean())
#     data_220 = db.Column(db.Boolean())
#     data_440 = db.Column(db.Boolean())
#     nbems_hf = db.Column(db.Boolean())
#     nbems_6m = db.Column(db.Boolean())
#     nbems_220 = db.Column(db.Boolean())
#     nbems_440 = db.Column(db.Boolean())
#     dstar_hf = db.Column(db.Boolean())
#     dstar_6m = db.Column(db.Boolean())
#     dstar_220 = db.Column(db.Boolean())
#     dstar_440 = db.Column(db.Boolean())
#     winlink_hf = db.Column(db.Boolean())
#     winlink_6m = db.Column(db.Boolean())
#     winlink_220 = db.Column(db.Boolean())
#     winlink_440 = db.Column(db.Boolean())
#     other = db.Column(db.String(300), unique=False, nullable=True)
