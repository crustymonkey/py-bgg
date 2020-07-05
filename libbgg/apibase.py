
from libbgg.infodict import InfoDict
from urllib.request import build_opener
from urllib.parse import urlencode, quote
import time

class BGGBase(object):
    def __init__(self, url_base='http://www.boardgamegeek.com', 
            path_base=''):
        """
        Set up the basic url stuff for retrieving items via the api
        
        url_base:str        The base url, including the http:// portion
        path_base:str       The base portion of the uri
        """
        self.url_base = url_base.rstrip('/')
        self.path_base = path_base.strip('/')
        self._base = '{}/{}'.format(self.url_base, self.path_base)
        self._base = self._base.rstrip('/')
        self._opener = self._get_opener()

    def _get_opener(self):
        """
        This returns a basic opener.  If auth is ever needed, this is the
        place it would be implemented
        """
        o = build_opener()
        return o
    
    def call(self, call_type, call_dict, wait=False):
        """
        This handles all of the actual calls to the bgg api.  It takes the
        first portion of the url and appends it to the base, then builds
        the query string from the call_dict after filtering None values.

        call_type:str       The path addition to append to the base url
        call_dict:dict      This is a dictionary mapping to be turned into
                            a query string
        wait:bool           This will cause the api to retry if a 202 is
                            returned until a 200 is returned.  This is
                            needed for the async calls for get_collection()

        returns InfoDict    Returns a mapping of items from the native XML
                            to a dictionary mapping
        """
        # First, filter any None values from the list
        for key, val in list(call_dict.items()):
            if val is None:
                del call_dict[key]

        url = '{}/{}?{}'.format(
            self._base,
            quote(call_type), 
            urlencode(call_dict),
        )
        res = self._opener.open(url)
        resp_str = res.read()

        if wait and res.code == 202:
            time.sleep(1)
            return self.call(call_type, call_dict, wait)

        return InfoDict.xml_to_info_dict(resp_str, strip_errors=True)
