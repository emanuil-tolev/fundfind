import uuid
from pyes.exceptions import ElasticSearchException

from flask import Blueprint, request, url_for, flash, redirect
from flask import render_template
from flask.ext.login import login_user, logout_user
from flask.ext.wtf import Form, TextField, PasswordField, validators

from fundfind import dao
from fundfind import util

blueprint = Blueprint('account', __name__)


@blueprint.route('/')
def index():
    return 'Accounts management index route.'

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        username = form.username.data
        user = None

        try:
            user = dao.Account.pull(username)
        except ElasticSearchException:
            pass # the else below will catch it
            # Not putting a specific message here since we don't want login
            # attempts to know they've got an existing username, but the
            # wrong password!

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Welcome back', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username/password', 'error')
    if request.method == 'POST' and not form.validate():
        flash('Invalid form', 'error')
    return render_template('account/login.html', form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))


class RegisterForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=25)])
    email = TextField('Email Address', [validators.Length(min=3, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    country = TextField('Country')
    organisation = TextField('Organisation')
    department = TextField('Department')
    research_group = TextField('Research Group')
    interests = TextField('Research interests')

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: re-enable csrf
    form = RegisterForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        api_key = str(uuid.uuid4())
        account = dao.Account(
            id=form.username.data,
            email=form.email.data,
            api_key=api_key,
            country=form.country.data,
            organisation=form.organisation.data,
            department=form.department.data,
            research_group=form.research_group.data,
            interests=util.clean_list( form.interests.data.split(',') )
        )
        account.set_password(form.password.data)
        account.save()
        login_user(account, remember=True)
        flash('Thanks for signing-up', 'success')
        return redirect(url_for('home'))
    if request.method == 'POST' and not form.validate():
        flash('Please correct the errors', 'error')
    return render_template('account/register.html', form=form)

