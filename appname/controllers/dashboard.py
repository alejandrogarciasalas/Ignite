from flask_login import login_required, current_user

from flask import Blueprint, render_template, flash, redirect, url_for, Markup

from appname.constants import REQUIRE_EMAIL_CONFIRMATION
from appname.models import db
from appname.forms.login import ChangePasswordForm

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
def check_for_confirmation(*args, **kwargs):
    if REQUIRE_EMAIL_CONFIRMATION:
        # If we have a logged in user, we can check if they have confirmed their email or not.
        if not current_user.is_authenticated or current_user.email_confirmed:
            return
        resend_confirm_link = url_for('auth.resend_confirmation')
        text = Markup(
            'Please confirm your email. '
            '<a href="{}" class="alert-link">Click here to resend</a>'.format(resend_confirm_link))
        flash(text, 'warning')

@dashboard.route('/dashboard')
@login_required
def home():
    return render_template('dashboard/home.html')

@dashboard.route('/dashboard/settings')
@login_required
def settings():
    # TODO: Implement @fresh_login_required for non-oauthed users (users with a password)
    form = ChangePasswordForm()
    return render_template('dashboard/settings.html', form=form)

@dashboard.route('/dashboard/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash("Changed password", "success")
    else:
        flash("The password was invalid", "warning")

    return redirect(url_for("dashboard.settings"))
