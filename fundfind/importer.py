from datetime import datetime

from jinja2 import Markup

import fundfind.dao
import fundfind.util as util


# inspired by http://oag.cottagelabs.com/developers/api
CROWDSOURCE_CONTRIB_LICENSE = {
    "type": "cc-by",
    "version": "3.0",
    "url": "http://creativecommons.org/licenses/by/3.0/",
    "title": "Creative Commons Attribution",
    'BY': True,
    'NC': False,
    'SA': False,
    'ND': False 

}

class Importer(object):
    def __init__(self, owner):
        self.owner = owner

    def describe_funder(self, request, id_=None):
        '''Import information about a funder into the index.'''
        
        
        tmpl = util.clean_list(request.values.getlist('useful_links[]'))
        useful_links = []
        for link in tmpl:
            useful_links.append(util.prep_link(link))
            
        if not id_:
            id_ = util.slug_id(request.values['name'])

        record = {
            "id": id_,
            "name": request.values['name'], # guaranteed to have 'name'
            "homepage": util.prep_link(request.values.get("homepage",'')),
            "description": request.values.get("description",''),
            "interested_in": request.values.get("interested_in",''),
            "policies": request.values.get("policies",''),
            "useful_links": useful_links,
            "tags": util.clean_list(request.values.get("tags",'').split(",")), 
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "owner": self.owner.id,
            "license": CROWDSOURCE_CONTRIB_LICENSE,
            "origin": "crowdsourced"
        }
        
        fundfind.dao.Funder.upsert(record)
        return id_
        
    def share_fundopp(self, request, id_=None):
        '''Import information about a funding opportunity into the index.'''
        
        
        tmpl = util.clean_list(request.values.getlist('useful_links[]'))
        useful_links = []
        for link in tmpl:
            useful_links.append(util.prep_link(link))
        
        if not id_:
            id_ = util.slug_id(request.values["title"])

        record = {
            "funder": request.values.get("funder", ''),
            "title": request.values["title"],
            "id": id_,
            "url": util.prep_link(request.values.get("url",'')),
            "description": Markup.escape(request.values.get("more_info",'')),
            "issue_date": request.values.get('issue_date',None),
            "closing_date": request.values.get('closing_date',None),
            "funds": request.values.get('funds',''),
            "funds_exactly_or_upto": request.values.get('funds_exactly_or_upto',''),
            "useful_links": useful_links,
            "tags": util.clean_list(request.values.get("tags",'').split(",")), 
            "of_interest_to": util.clean_list(request.values.get("of_interest_to",'').split(",")), 
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "owner": self.owner.id,
            "license": CROWDSOURCE_CONTRIB_LICENSE,
            "origin": "crowdsourced"
        }

        # cause ElasticSearch exceptions if null or empty string
        # so just remove them from the document
        if not record['issue_date']: del record['issue_date']
        if not record['closing_date']: del record['closing_date']
        
        fundfind.dao.FundingOpp.upsert(record)
        return id_
