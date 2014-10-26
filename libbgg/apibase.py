
from .infodict import InfoDict
import urllib2 , urllib

class BGGBase(object):
    def __init__(self , url_base='http://www.boardgamegeek.com' , 
            path_base=''):
        """
        Set up the basic url stuff for retrieving items via the api
        
        url_base:str        The base url, including the http:// portion
        path_base:str       The base portion of the uri
        """
        self.url_base = url_base.rstrip('/')
        self.path_base = path_base.strip('/')
        self._base = '%s/%s' % (self.url_base , self.path_base)
        self._base = self._base.rstrip('/')
        self._opener = self._get_opener()

    def _get_opener(self):
        """
        This returns a basic opener.  If auth is ever needed, this is the
        place it would be implemented
        """
        o = urllib2.build_opener()
        return o
    
    def call(self , call_type , call_dict):
        url = '%s/%s?%s' % (self._base , urllib.quote(call_type) , 
            urllib.urlencode(call_dict))
        res = self._opener.open(url)
        resp_str = res.read()
        return InfoDict.xml_to_info_dict(resp_str)
