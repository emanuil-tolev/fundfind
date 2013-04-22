from parsedatetime import parsedatetime as pdt

import urllib2
from datetime import datetime
from cStringIO import StringIO

import fundfind.dao
import fundfind.util as util

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
        }
        
        fundfind.dao.Funder.upsert(record)
        
    def share_fundopp(self, request):
        '''Import information about a funding opportunity into the index.'''
        
        
        tmpl = util.clean_list(request.values.getlist('useful_links[]'))
        useful_links = []
        for link in tmpl:
            useful_links.append(util.prep_link(link))
            
        record = {
            "title": request.values.get("title", ''),
            "short_desc": request.values.get('unique_title', util.slugify(request.values.get("title", '')) ),
            "url": util.prep_link(request.values.get("url",''), endslash=True),
            "description": request.values.get("description",''),
#            "issue_date": util.str2isodt(request.values.get('issue_date','')),
#            "closing_date": util.str2isodt(request.values.get('closing_date','')),
            "issue_date": request.values.get('issue_date',''),
            "closing_date": request.values.get('closing_date',''),
            "funds": request.values.get('funds',''),
            "funds_exactly_or_upto": request.values.get('funds_exactly_or_upto',''),
            "more_info": request.values.get('more_info',''),
            "useful_links": useful_links,
            "tags": util.clean_list(request.values.get("tags",'').split(",")), 
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "owner": self.owner.id,
        }
        
        fundfind.dao.FundingOpp.upsert(record)