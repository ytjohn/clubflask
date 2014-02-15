# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_required
from clubflask.user.forms import ProfileForm
from clubflask.utils import flash_errors


blueprint = Blueprint("user", __name__, url_prefix='/users',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("users/members.html")

    
@blueprint.route("/profile/", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(request.form, csrf_enabled=True)
    if form.validate_on_submit():
        # new_user = User.create(username=form.username.data,
        #                 email=form.email.data,
        #                 password=form.password.data,
        #                 active=True)
        
        flash("Thank you for your data. It's not saved yet.", 'success')
        return redirect(url_for('user.profile'))
    else:
        flash_errors(form)
    return render_template('users/profile.html', form=form)