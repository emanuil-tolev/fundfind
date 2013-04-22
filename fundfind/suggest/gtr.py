import requests
from urllib import urlencode
import json # for parsing the answer

BASE_SVC_URL = 'http://gtr.rcuk.ac.uk'
SVC_ACTION = 'search'
SVC_FORMAT_REQ = '.json'
SVC_URL_SEPARATOR = '/'

def suggest_projects(similar_to):
    SVC_RESOURCE = 'project'
    
    url = _build_svc_url(
        BASE_SVC_URL,
        SVC_ACTION,
        SVC_RESOURCE,
        SVC_FORMAT_REQ,
        SVC_URL_SEPARATOR,
        {'term': similar_to}
    )
    try:
        results = requests.get(url)
        
        if results.status_code not in [200]:
            return _make_error('Suggestions problem. Remote server returned {0.status_code}.'.format(results))
        
        try:
            return json.loads(results.text)
        except ValueError as e:
            return _make_error('Suggestions problem. Could not decode remote server\' response as valid JSON.')
        
    except RequestException as e:
        # something's wrong, e.g. nonexistent or malformed URL, timeout, etc.
        return _make_error('A problem has occured while trying to get suggestions from the GTR API over HTTP. Problem: {0}'.format(e))

def _make_error(msg):
    return {'error': msg}
        
def _build_svc_url(base_url, action, resource, req_format, url_sep, terms={}):
    url = url_sep.join([base_url, action, resource])
    url = url + req_format
    
    query_string = '?' + urlencode(terms)
    url = url + query_string
    
    return url