
from libbgg.apibase import BGGBase
from libbgg.errors import InvalidInputError, APICallError
from datetime import date

class BGG(BGGBase):

    things = ('boardgame', 'boardgameexpansion', 'videogame', 'rpgitem', 
        'rpgissue')
    family_types = ('rpg', 'rpgperiodical', 'boardgamefamily')

    def __init__(self, url_base='http://www.boardgamegeek.com', 
            path_base='xmlapi2'):
        super(BGG, self).__init__(url_base, path_base)
        self._last_called = None

    def __getattr__(self, name):
        self._last_called = name
        if name in self.things:
            return self._things
        elif name in self.family_types:
            return self._family_items
        raise AttributeError('%s is not a valid name' % name)

    def _family_items(self, fid, ftype=None):
        """
        This handles all the calls for "family items" as defined by the
        BGG API: http://boardgamegeek.com/wiki/page/BGG_XML_API2
        """
        if ftype is None:
            ftype = self._last_called
        elif isinstance(ftype, (list, tuple)):
            ftype = ','.join(ftype)
        if isinstance(fid, (list, tuple)):
            fid = ','.join([ str(i) for i in fid ])
        d = {'id': fid, 'type': ftype}
        return self.call('family', d)

    def _things(self, bid, ttype=None, versions=True, videos=True,
            stats=True, historical=True, marketplace=True, comments=True,
            ratingcomments=True, page=1, pagesize=50):
        """
        This handles all the calls for "things" as defined by the
        BGG API: http://boardgamegeek.com/wiki/page/BGG_XML_API2
        """
        if ttype is None:
            ttype = self._last_called
        elif isinstance(ttype, (list, tuple)):
            ttype = ','.join(ttype)
        if isinstance(bid, (list, tuple)):
            bid = ','.join([ str(i) for i in bid ])
        d = {'id': bid, 'type': ttype, 'versions': int(versions), 
            'videos': int(videos), 'stats': int(stats), 
            'historical': int(historical), 'marketplace': int(marketplace),
            'comments': int(comments), 'ratingcomments': int(ratingcomments),
            'page': page, 'pagesize': pagesize,
        }
        return self.call('thing', d)

    def search(self, search_str, qtype='boardgame', exact=False):
        """
        Search for board games by string.  If exact is true, only exact
        matches will be returned
        
        search_str:str          The string to search for
        qtype:str               One of the "things"
        exact:bool              Match the string exactly
        """
        if qtype not in self.things:
            raise InvalidInputError('The qtype must be one of %r' % 
                self.things)
        d = { 'query': search_str, 'type': qtype, 'exact': int(exact) }
        return self.call('search', d)
