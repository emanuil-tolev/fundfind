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
        
        
        tmpl = self._clean_list(request.values.getlist('useful_links[]'))
        useful_links = []
        for link in tmpl:
            useful_links.append(self._prep_link(link))
            
        record = {
            "name": request.values['name'], # guaranteed to have 'name'
            "homepage": self._prep_link(request.values.get("homepage",''), endslash=True),
            "description": request.values.get("description",''),
            "interested_in": request.values.get("interested_in",''),
            "policies": request.values.get("policies",''),
            "useful_links": useful_links,
            "tags": self._clean_list(request.values.get("tags",'').split(",")), 
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "owner": self.owner.id,
        }
        
        fundfind.dao.Funder.upsert(record)
        
    def _clean_list(self, list):
        '''Clean up a list coming from an HTML form. Returns a list.
        Returns an empty list if given an empty list.
        
        How to use: clean_list = self._clean_list(your_list), can use anywhere
        in this class where you've got a list.

        Example: you have a list of tags. This is coming in from the form
        as a single string: e.g. "tag1, tag2, ".
        You do tag_list = request.values.get("tags",'').split(",")
        Now you have the following list: ["tag1"," tag2", ""]
        You want to both trim the whitespace from list[1] and remove the empty
        element - list[2]. self._clean_list(tag_list) will do it.
        
        What it does (a.k.a. algorithm):
        1. Trim whitespace on both ends of individual strings
        2. Remove empty strings
        3. Only check for empty strings AFTER splitting and trimming the 
        individual strings (in order to remove empty list elements).
        '''
        # consider moving this method out to dao.py or somewhere where it can
        # be reused more easily - it is really generic
        return [clean_item for clean_item in [item.strip() for item in list] if clean_item]
        
    def _prep_link(self, link, endslash=False):
        '''Prepare a string which is meant to be a link (HTTP URL) for
        indexing. Puts http:// at the front if the string it's passed does not
        already start with http:// or https://.
        
        The endslash parameter is a Boolean which controls whether a forward
        slash '/' will be added to the string if the string doesn't already
        end with a '/'.
        
        Returns an empty string if passed an empty string (so you will never
        end up with 'http:///' or something of the sort).
        '''
        if link:
            if endslash and not link.endswith('/'):
                link += '/'
            if not ( link.startswith('http://') or link.startswith('https://') ):
                link = 'http://' + link
            
        return link