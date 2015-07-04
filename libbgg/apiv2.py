
from libbgg.apibase import BGGBase
from libbgg.errors import InvalidInputError, APICallError
from datetime import date

class BGG(BGGBase):
    """
    For version 2 of the api, you simply instantiate the object and call
    the appropriate method. "things" and "family items" are handled
    dynamically and are not completely documented.

    Example:

    from libbgg.apiv2 import BGG

    bgg = BGG()
    # Get a boardgame:
    game_tree = bgg.boardgame(game_id, stats=True, ratingcomments=True)
    # You can also get multiple games in a single call (Recommended)
    ids = [16881, 16882, 16883]
    game_trees = bgg.boardgame(ids, stats=True)

    Use the same pattern to get board game expansions, rpgs, etc.

    game_tree = bgg.boardgameexpansion(game_id, stats=True)
    """

    things = ('boardgame', 'boardgameexpansion', 'videogame', 'rpgitem', 
        'rpgissue')
    family_types = ('rpg', 'rpgperiodical', 'boardgamefamily')
    user_domains = ('boardgame', 'rpg', 'videogame')
    guild_sorts = ('username', 'date')

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

    def _things(self, bid, ttype=None, versions=False, videos=False,
            stats=False, historical=False, marketplace=False, comments=False,
            ratingcomments=False, page=1, pagesize=50):
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

    def forum_lists(self, gid, ftype='thing'):
        if isinstance(gid, (list, tuple)):
            gid = ','.join([ str(i) for i in gid ])

        if ftype not in ('thing', 'family'):
            raise InvalidInputError('Forum type must be either "thing" or '
                '"family"')
        d = { 'id': gid, 'type': ftype }
        return self.call('forumlist', d)

    def forums(self, fid, page=1):
        if isinstance(fid, (list, tuple)):
            fid = ','.join([ str(i) for i in fid ])

        page = int(page)
        d = { 'id': fid, 'page': page }
        return self.call('forum', d)

    def threads(self, tid, min_article_id=None, min_article_date=None,
            count=None, username=None):
        if isinstance(tid, (list, tuple)):
            tid = ','.join([ str(i) for i in tid ])

        d = { 'id': tid }

        if min_article_id is not None:
            d['minarticleid'] = int(min_article_id)
        if min_article_date is not None:
            d['minarticledate'] = min_article_date
        if count is not None:
            d['count'] = int(count)
        if username is not None:
            d['username'] = username

        return self.call('thread', d)

    def user(self, username, buddies=False, guilds=False, hot=False,
            top=False, domain='boardgame', page=1):
        if domain is not None and domain not in self.user_domains:
            raise InvalidInputError('User domain must be one of {}'.format(
                ', '.join(self.user_domains)))
        d = {
            'name': username, 
            'buddies': int(buddies), 
            'guilds': int(guilds),
            'hot': int(hot), 
            'top': int(top), 
            'domain': domain,
            'page': int(page),
        }
        
        return self.call('user', d)

    def guilds(self, gid, members=False, sort='username', page=1):
        if isinstance(gid, (list, tuple)):
            gid = ','.join([ str(i) for i in gid ])

        if sort is not None and sort not in self.guild_sorts:
            raise InvalidInputError('Guild sort types must be one of '
                '{}'.format(', '.join(self.guild_sorts)))

        d = {
            'id': gid,
            'members': int(members),
            'sort': sort,
            'page': int(page),
        }

        return self.call('guild', d)

    #def plays(self, 
