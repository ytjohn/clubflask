# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required, current_user
from clubflask.user.forms import ProfileForm
from clubflask.utils import flash_errors
from clubflask.user.models import User, Profile, Privacy
from clubflask.database import db

blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("users/members.html")

    
@blueprint.route("/profile/", methods=['GET', 'POST'])
@login_required
def profile():
    # print current_user
    user_id = current_user.id
    userprofile = Profile.query.filter_by(user_id=user_id).first()
    privacyoptions = Privacy.query.filter_by(user_id=user_id).first()
    if not privacyoptions:
        privacyoptions = Privacy.create(user_id=user_id)
    
    form = ProfileForm(request.form, userprofile, csrf_enabled=True)
    
    # mix in privacy privacyoptions
    # form.enrollinwpaares.data = privacyoptions.enrollinwpaares   
    # form.addtomailinglist.data = privacyoptions.addtomailinglist
    # form.sharewithclub.data = privacyoptions.sharewithclub
    
    if form.validate_on_submit():
        db.session.add(userprofile)
        userprofile.first_name = form.first_name.data
        userprofile.last_name = form.last_name.data
        userprofile.callsign = form.callsign.data
        userprofile.licenseclass = form.licenseclass.data
        userprofile.mobilephone = form.mobilephone.data
        userprofile.homephone = form.homephone.data
        userprofile.address = form.address.data
        userprofile.city = form.city.data
        userprofile.state = form.state.data
        userprofile.zip = form.zip.data
        userprofile.county = form.county.data
        
        privacyoptions.sharewithclub = form.sharewithclub.data
        privacyoptions.enrollinwpaares = form.enrollinwpaares.data
        privacyoptions.addtomailinglist = form.addtomailinglist.data
        
        db.session.commit()
        
        # userprofile.callsign = form.callsign.data
        # new_user = User.create(username=form.username.data,
        #                 email=form.email.data,
        #                 password=form.password.data,
        #                 active=True)
        
        flash("Thank you for your update.", 'success')
        return redirect(url_for('user.profile'))
    else:
        flash_errors(form)
    return render_template('users/profile.html', form=form)