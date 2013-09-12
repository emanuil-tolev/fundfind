from parsedatetime import parsedatetime as pdt

from datetime import datetime

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

    def describe_funder(self, request):
        '''Import information about a funder into the index.'''
        
        
        tmpl = util.clean_list(request.values.getlist('useful_links[]'))
        useful_links = []
        for link in tmpl:
            useful_links.append(util.prep_link(link))
            
        record = {
            "id": util.slug_id(request.values['name']),
            "name": request.values['name'], # guaranteed to have 'name'
            "homepage": util.prep_link(request.values.get("homepage",''), endslash=True),
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
        
    def share_fundopp(self, request):
        '''Import information about a funding opportunity into the index.'''
        
        
        tmpl = util.clean_list(request.values.getlist('useful_links[]'))
        useful_links = []
        for link in tmpl:
            useful_links.append(util.prep_link(link))
            
        record = {
            "funder": request.values.get("funder", ''),
            "title": request.values["title"],
            "id": util.slug_id(request.values["title"]),
            "url": util.prep_link(request.values.get("url",''), endslash=True),
            "description": request.values.get("more_info",''),
            "issue_date": request.values.get('issue_date',''),
            "closing_date": request.values.get('closing_date',''),
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
        
        fundfind.dao.FundingOpp.upsert(record)
