import re
import json

from flask import Flask, jsonify, json, request, redirect, abort, make_response
from flask import render_template, flash
from flask.views import View, MethodView
from flask.ext.login import login_user, current_user

import fundfind.dao
import fundfind.importer
from fundfind.config import config
from fundfind.core import app, login_manager
from fundfind.view.account import blueprint as account

app.register_blueprint(account, url_prefix='/account')


# NB: the decorator appears to kill the function for normal usage
@login_manager.user_loader
def load_account_for_login_manager(userid):
    out = fundfind.dao.Account.get(userid)
    return out

@app.context_processor
def set_current_user():
    """ Set some template context globals. """
    return dict(current_user=current_user)

@app.before_request
def standard_authentication():
    """Check remote_user on a per-request basis."""
    remote_user = request.headers.get('REMOTE_USER', '')
    if remote_user:
        user = fundfind.dao.Account.get(remote_user)
        if user:
            login_user(user, remember=False)
    # add a check for provision of api key
    elif 'api_key' in request.values:
        res = fundfind.dao.Account.query(q='api_key:"' + request.values['api_key'] + '"')['hits']['hits']
        if len(res) == 1:
            user = fundfind.dao.Account.get(res[0]['_source']['id'])
            if user:
                login_user(user, remember=False)

@app.route('/')
def home():
    return render_template('home/index.html')

@app.route('/account/<user>')
def account(user):
    if hasattr(current_user,'id'):
        if user == current_user.id:
            return render_template('account/view.html',current_user=current_user, active_page='account')
    flash('You are not that user. Or you are not logged in.')
    return redirect('/account/login')

# Render static pages e.g. guides, tutorials, explanations...
@app.route('/content/<path:path>')
def content(path):
    return render_template('home/content.html', page=path)

# Search / faceted browsing interface
@app.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html', active_page='browse')

class DescribeFunderView(MethodView):
    '''Submit information about a funding organisation'''
    def get(self):
        if current_user.is_anonymous():
            flash('You need to login to be able to describe funders or funding opportunities.')
            return redirect('/account/login')
        if request.values.get("name") is not None:
            return self.post()
        return render_template('describe_funder.html', active_page='describe_funder')

    def post(self):
        if current_user.is_anonymous():
            abort(401)
            
        # TODO: need some better validation. see python flask docs for info.
        # TODO check if we already have this name as a funder
        if request.values.has_key('name') and request.values['name']:
            importer = fundfind.importer.Importer(owner=current_user)
            importer.describe_funder(request)
            flash('Successfully received funding organisation information')
            # TODO fix this when funders route is implemented
            # return redirect('/funders/' + request.values['name'])
            return redirect('/')
        else:
            flash('We need the name of the funding organisation')
            
            return render_template('describe_funder.html')

app.add_url_rule('/describe_funder', view_func=DescribeFunderView.as_view('describe_funder'))

class ShareFundoppView(MethodView):
    '''Submit information about a funding opportunity'''
    def get(self):
        if current_user.is_anonymous():
            flash('You need to login to be able to describe funders or funding opportunities.')
            return redirect('/account/login')
        if request.values.get("name") is not None:
            return self.post()
        return render_template('share_fundopp.html', active_page='share_fundopp')

    def post(self):
        if current_user.is_anonymous():
            abort(401)
            
        # TODO check if we already have this name as a fundopp
        if request.values.has_key('title') and request.values['title']:
            importer = fundfind.importer.Importer(owner=current_user)
            importer.share_fundopp(request)
            flash('Successfully received funding opportunity information')
            return redirect('/')
        else:
            flash('We need the title of the funding opportunity')
            
            return render_template('share_fundopp.html')

app.add_url_rule('/share_fundopp', view_func=ShareFundoppView.as_view('share_fundopp'))

@app.route('/slugify', methods=['GET','POST'])
def expose_slugify():
    '''Expose the slugify utility function to the world (to be used in 
    particular by AJAX requests showing the user what their string will look
    like after it is slugified.
    
    Used for generating unique identifiers from titles (e.g. of funding
    opportunities) and other such strings.'''
    # if the expected parameter is not found in the request, issue a
    # 400 Bad Request response
    if not request.values.has_key('make_into_slug'):
        abort(400)
    else:
        from fundfind.util import slugify as slugify
        return slugify(request.values['make_into_slug'])
        
@app.route('/suggest', methods=['GET','POST'])
def suggest():
    '''
    Use the suggest package to suggest relevant resources.
    This is a non-specific route which currently does the same as
    /suggest/projects (but can change to include other suggestion types).
    
    '''
    return suggest_projects()
    
@app.route('/suggest/projects', methods=['GET','POST'])
def suggest_projects():
    '''
    Use the suggest package to suggest projects relevant to the incoming
    similar_to parameter. This is the query the user inputs into facetview
    when fundfind uses it, but can be called like any other API route with
    arbitrary similar_to values.
    '''
    # need to know what to suggest
    if not request.values.has_key('similar_to'):
        abort(400)
    else:
        from fundfind.suggest import suggest_projects
        try:
            result = jsonify(suggest_projects(request.values['similar_to']))
        except ValueError as e:
            result = {'error': 'Suggestions problem. Could not encode suggestions in JSON to send to front-end.'}
        return result

if __name__ == "__main__":
    fundfind.dao.init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
