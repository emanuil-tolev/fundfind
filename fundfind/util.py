import re
import uuid
from unicodedata import normalize

def slug_id(string):
    """
    Generates a slug-like Elasticsearch id from a string, making
    sure it really is unique within the object's ES document type.

    Has to add a unique UUID4 to the slug for now, since collision
    resolution is quite a complex problem.
    """
    return slugify(string) + '.' + uuid.uuid4().hex

# derived from http://flask.pocoo.org/snippets/5/ (public domain)
# changed delimiter to _ instead of - due to ES search problem on the -
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'_'):
    """Generates a slightly worse ASCII-only slug."""
    result = []
    text = unicode(text, errors="ignore")
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def clean_list(list):
    '''Clean up a list. Returns a list.
    Returns an empty list if given an empty list.
    
    How to use: clist = clean_list(your_list)

    Example: you have a list of tags. This is coming in from an HTML form
    as a single string: e.g. "tag1, tag2, ".
    You do tag_list = request.values.get("tags",'').split(",")
    Now you have the following list: ["tag1"," tag2", ""]
    You want to both trim the whitespace from list[1] and remove the empty
    element - list[2]. clean_list(tag_list) will do it.
    
    What it does (a.k.a. algorithm):
    1. Trim whitespace on both ends of individual strings
    2. Remove empty strings
    3. Only check for empty strings AFTER splitting and trimming the 
    individual strings (in order to remove empty list elements).
    '''
    return [clean_item for clean_item in [item.strip() for item in list] if clean_item]
    
def prep_link(link, endslash=False):
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
    

# The whole str2isodt (originally named datetimeFromString) helper method 
# is taken from
# http://stackoverflow.com/questions/1810432/handling-the-different-results-from-parsedatetime
# The parsedatetime 3rd party package for parsing human-readable dates
# returns different types of values from its parse() method, but we only
# care for Python native datetime objects, so this helper is used to
# convert whatever parsedatetime returns to native datetime.

def str2isodt(s):
    if not s.strip():
        return None

    c = pdt.Calendar()
    result, what = c.parse( s )

    dt = None

    # what was returned (see http://code-bear.com/code/parsedatetime/docs/)
    # 0 = failed to parse
    # 1 = date (with current time, as a struct_time)
    # 2 = time (with current date, as a struct_time)
    # 3 = datetime
    if what in (1,2):
        # result is struct_time
        dt = datetime.datetime( *result[:6] )
    elif what == 3:
        # result is a datetime
        dt = result

    if dt is None:
        # Failed to parse
        raise ValueError, ("Don't understand date '"+s+"'")

    return dt.isoformat()
