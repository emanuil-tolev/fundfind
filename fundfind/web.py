import re
import json
from pyes.exceptions import ElasticSearchException

from flask import Flask, jsonify, json, request, redirect, abort, make_response, url_for
from flask import render_template, flash
from flask.views import View, MethodView
from flask.ext.login import login_user, current_user

import fundfind.dao
import fundfind.importer
from fundfind.config import config
from fundfind.core import app, login_manager
from fundfind.view.account import logout
from fundfind.view.account import blueprint as account

app.register_blueprint(account, url_prefix='/account')


# NB: the decorator appears to kill the function for normal usage
@login_manager.user_loader
def load_account_for_login_manager(userid):
    try:
        out = fundfind.dao.Account.get(userid)
    except ElasticSearchException:
        flash('Your account was deleted while you were logged in. (?!)', 'error')
        return None
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

@app.route('/account/<user>')
def account(user):
    if hasattr(current_user,'id'):
        if user == current_user.id:
            return render_template('account/view.html',current_user=current_user, active_page='account', page_title='Your Account')
    flash('You are not that user. Or you are not logged in.')
    return redirect('/account/login')

# Render static pages e.g. guides, tutorials, explanations...
@app.route('/content/<path:path>')
def content(path):
    return render_template('home/content.html', page=path)

# Search / faceted browsing interface
@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html', active_page='search',
        es_host=config['ELASTIC_SEARCH_HOST'],
        es_index=config['ELASTIC_SEARCH_DB'],
        page_title='Browse & Search FundFind'
    )

@app.route('/funding_opportunities/<path:path>')
def show_funding_opportunity(path):
    renderobj = fundfind.dao.FundingOpp.get(path)
    return render_template('show.html', o=renderobj, page_title=renderobj['title'])

class DescribeFunderView(MethodView):
    '''Submit information about a funding organisation'''
    def get(self, req_format='html'):
        if current_user.is_anonymous():
            if req_format == 'json':
                return jsonify({'error': 'You need to specify api_key in the request data. Only registered users can submit funder or funding opportunity data.'})
            else:
                flash('You need to login to be able to describe funders or funding opportunities.')
                return redirect('/account/login')

        if request.values.get("name") is not None:
            return self.post(req_format)

        if req_format == 'json':
            return jsonify({'error': 'You need to POST to this URL if using the API.'})
        else:
            return render_template('describe_funder.html', active_page='describe_funder', page_title='Describe a Funding Organisation')

    def post(self, req_format='html'):
        if current_user.is_anonymous():
            abort(401)
            
        if request.values.has_key('name') and request.values['name']:
            importer = fundfind.importer.Importer(owner=current_user)
            importer.describe_funder(request)
            if req_format == 'json':
                return jsonify({'ok': True})
            else:
                flash('Successfully received funding organisation information')
                return redirect('/')
        else:
            error_msg = 'We need the name of the funding organisation'
            if req_format == 'json':
                return jsonify({'error': error_msg})
            else:
                flash(error_msg)
                return render_template('describe_funder.html', page_title='Describe a Funding Organisation')

app.add_url_rule('/describe_funder', view_func=DescribeFunderView.as_view('describe_funder'))
app.add_url_rule('/describe_funder.<req_format>', view_func=DescribeFunderView.as_view('describe_funder'))

class ShareFundoppView(MethodView):
    '''Submit information about a funding opportunity'''
    def get(self, req_format='html', path=None):
        if current_user.is_anonymous():
            if req_format == 'json':
                return jsonify({'error': 'You need to specify api_key in the request data. Only registered users can submit funder or funding opportunity data.'})
            else:
                flash('You need to login to be able to describe funders or funding opportunities.')
                return redirect('/account/login')

        if request.values.get("name") is not None:
            return self.post(req_format, path)

        if req_format == 'json':
            return jsonify({'error': 'You need to POST to this URL if using the API.'})

        renderobj = None
        title = 'Share a Funding Opportunity'
        if path:
            renderobj = fundfind.dao.FundingOpp.get(path)
            title = 'Edit Funding Opportunity :: ' + renderobj['title']

        return render_template('share_fundopp.html', active_page='share_fundopp', o=renderobj, page_title=title)

    def post(self, req_format='html'):
        if current_user.is_anonymous():
            abort(401)
        
        if request.values.has_key('title') and request.values['title']:
            importer = fundfind.importer.Importer(owner=current_user)
            if 'id' in request.values:
                id_ = importer.share_fundopp(request, id_=request.values['id'])
            else:
                id_ = importer.share_fundopp(request)

            if req_format == 'json':
                return jsonify({'ok': True})
            else:
                flash('Successfully received funding opportunity information')
                return redirect(url_for("show_funding_opportunity", path=id_))
        else:
            error_msg = 'We need the title of the funding opportunity'
            if req_format == 'json':
                return jsonify({'error': error_msg})
            else:
                flash(error_msg)
                return render_template('share_fundopp.html', page_title='Share a Funding Opportunity')

app.add_url_rule('/share_fundopp', view_func=ShareFundoppView.as_view('share_fundopp'))
app.add_url_rule('/share_fundopp.<req_format>', view_func=ShareFundoppView.as_view('share_fundopp'))
app.add_url_rule('/share_fundopp/<path:path>', view_func=ShareFundoppView.as_view('share_fundopp'))

@app.route('/slugify', methods=['GET','POST'])
@app.route('/slugify.<req_format>', methods=['GET','POST'])
def expose_slugify(req_format=None):
    '''
    Expose the slugify utility function to the world (to be used in 
    particular by AJAX requests showing the user what their string will look
    like after it is slugified.
    
    Used for generating unique identifiers from titles (e.g. of funding
    opportunities) and other such strings.
    '''

    if not request.values.has_key('make_into_slug'):
        abort(400)
    else:
        from fundfind.util import slugify as slugify
        slug = slugify(request.values['make_into_slug'])
        if req_format == 'json':
            return jsonify({'slug': slug})
        else:
            return slug
        
@app.route('/suggest', methods=['GET','POST'])
@app.route('/suggest.<req_format>', methods=['GET','POST'])
def suggest(req_format='json'):
    '''
    Use the suggest package to suggest relevant resources.
    This is a non-specific route which currently does the same as
    /suggest/projects (but can change to include other suggestion types).
    
    '''
    return suggest_projects(req_format)
    
@app.route('/suggest/projects', methods=['GET','POST'])
@app.route('/suggest/projects.<req_format>', methods=['GET','POST'])
def suggest_projects(req_format='json'):
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
            result = suggest_projects(request.values['similar_to'])
        except ValueError as e:
            result = {'error': 'Suggestions problem. Could not encode suggestions in JSON to send to front-end.'}
        return jsonify(result)

@app.route('/')
@app.route('/.<req_format>')
def home(req_format='html'):
    if req_format == 'json':
        # TODO enumerate the available routes programmatically
        # TODO implement actual OPTIONS
        return jsonify({'options': ['/share_fundopp', '/describe_funder', '/suggest', '/suggest/projects', '/slugify']})
    return render_template('home/index.html', page_title='FundFind - Welcome!')

@app.route('/feedback')
def feedback_info():
    return render_template('feedback.html', active_page="feedback", page_title='Feedback for FundFind')

# custom template filter definitions
def nl2br(value): 
    return value.replace('\n','<br>\n')

# custom template function definitions
def query_source(**kwargs):
    return fundfind.dao.DomainObject.q2json(fundfind.dao.DomainObject.generate_query(**kwargs))

# customise the jinja environment here
app.jinja_env.filters['nl2br'] = nl2br
app.jinja_env.globals.update(query_source=query_source)

if __name__ == "__main__":
    fundfind.dao.init_db()
    app.run(host='0.0.0.0', port=5001, debug=config['debug'])
