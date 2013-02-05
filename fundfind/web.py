import re
import json

from flask import Flask, jsonify, json, request, redirect, abort, make_response
from flask import render_template, flash
from flask.views import View, MethodView
from flask.ext.login import login_user, current_user

import fundfind.identifier
import fundfind.dao
import fundfind.iomanager
import fundfind.importer
from fundfind.config import config
from fundfind.core import app, login_manager
from fundfind.view.account import blueprint as account
from fundfind import auth

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


@app.template_filter('dtformat')
def datetimeformat(value, format='%d-%B-%Y %H:%M:%S'):
    return value#.strftime(format)
                
@app.route('/')
def home():
    return render_template('home/index.html')

@app.route('/account/<user>')
def account(user):
    if hasattr(current_user,'id'):
        if user == current_user.id:
            return render_template('account/view.html',current_user=current_user)
    flash('You are not that user. Or you are not logged in.')
    return redirect('/account/login')

@app.route('/content/<path:path>')
def content(path):
    return render_template('home/content.html', page=path)

class RateView(MethodView):
    def get(self):
        if not auth.collection.create(current_user, None):
            flash('You need to login to rate a regex')
            return redirect('/account/login')
        if request.values.get("test_worked") is not None:
            return self.post()
            
        tests = fundfind.dao.Test.query() # get all the tests
        tests = tests['hits']['hits']

        return render_template('rate.html', tests=tests)

    def post(self):
        if not auth.collection.create(current_user, None):
            abort(401)
        importer = fundfind.importer.Importer(owner=current_user)
        importer.rate(request)
        flash('Successfully received your rating')
        return redirect('/')

app.add_url_rule('/rate', view_func=RateView.as_view('rate'))


class DescribeFunderView(MethodView):
    '''Submit information about a funding organisation'''
    def get(self):
        if not auth.collection.create(current_user, None):
            flash('You need to login to be able to describe funders or funding opportunities.')
            return redirect('/account/login')
        if request.values.get("name") is not None:
            return self.post()
        return render_template('describe_funder.html')

    def post(self):
        if not auth.collection.create(current_user, None):
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
        if not auth.collection.create(current_user, None):
            flash('You need to login to be able to describe funders or funding opportunities.')
            return redirect('/account/login')
        if request.values.get("name") is not None:
            return self.post()
        return render_template('share_fundopp.html')

    def post(self):
        if not auth.collection.create(current_user, None):
            abort(401)
            
        # TODO: need some better validation. see python flask docs for info.
        # TODO check if we already have this name as a fundopp
        if request.values.has_key('title') and request.values['title']:
            importer = fundfind.importer.Importer(owner=current_user)
            importer.share_fundopp(request)
            flash('Successfully received funding opportunity information')
            # TODO fix this when fundopps route is implemented
            # return redirect('/fundopps/' + request.values['short_title'])
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

def outputJSON(results, record=False):
    '''build a JSON response, with metadata unless specifically asked to suppress'''
    # TODO: in some circumstances, people data should be added to collections too.
    out = {"metadata":{}}
    out['metadata']['query'] = request.base_url + '?' + request.query_string
    out['records'] = results
    out['metadata']['from'] = request.values.get('from',0)
    out['metadata']['size'] = request.values.get('size',10)

    resp = make_response( json.dumps(out, sort_keys=True, indent=4) )
    resp.mimetype = "application/json"
    return resp

if __name__ == "__main__":
    fundfind.dao.init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)

