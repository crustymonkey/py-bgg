
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
    ids = (16881, 16882, 16883)
    game_trees = bgg.boardgame(ids, stats=True)

    Use the same pattern to get board game expansions, rpgs, etc.

    game_tree = bgg.boardgameexpansion(game_id, stats=True)
    print game_tree['items']['item']['description']['TEXT']

    You can also access things as properties when the property does not
    conflict with a dictionary propert e.g. "items"
    game = game_tree['items']['item']
    print game.description.TEXT
    print game.minplayers.value
    etc.

    """

    things = ('boardgame', 'boardgameexpansion', 'videogame', 'rpgitem', 
        'rpgissue')
    family_types = ('rpg', 'rpgperiodical', 'boardgamefamily')
    forum_list_types = ('thing', 'family')
    user_domains = ('boardgame', 'rpg', 'videogame')
    guild_sorts = ('username', 'date')
    play_types = ('thing', 'family')
    play_subtypes = ('boardgame', 'boardgameexpansion', 'videogame', 'rpgitem')
    search_types = play_subtypes
    hot_types = ('boardgame', 'rpg', 'videogame', 'boardgameperson',
        'rpgperson', 'boardgamecompany', 'rpgcompany', 'videogamecompany')

    def __init__(self, url_base='http://www.boardgamegeek.com', 
            path_base='xmlapi2'):
        super(BGG, self).__init__(url_base, path_base)
        self._last_called = None

    def __getattr__(self, name):
        """
        This is a magic method to handle calls to the instance like
        instance.boardgame() or instance.boardgameexpansion()
        """
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
        qtype:str|list[str]     One of the "things"
        exact:bool              Match the string exactly
        """
        if not isinstance(qtype, (list, tuple)):
            qtype = [qtype]

        invalid_types = set(qtype) - set(self.search_types)
        if invalid_types:
            raise InvalidInputError('The qtypes must be one of {}, invalid '
                'item(s) submitted: ({})'.format(self.search_types,
                ', '.join(invalid_types)))

        d = { 'query': search_str, 'type': ','.join(qtype),
            'exact': int(exact) }
        return self.call('search', d)

    def get_collection(self, username, wait=True, **kwargs):
        """
        This will retrieve a user's collection, with optional flags set.
        There are just too many options here to have individual options
        listed here.  You can specify any of the options in your call
        like so: 
        
        obj.get_collection('username', own=1, played=1)

        All the options are listed on the documentation page for the API
        at http://boardgamegeek.com/wiki/page/BGG_XML_API#toc4

        username:str        The username to retrieve the collection for
        wait:bool           Wait for the collection to be loaded before
                            returning from this function.  If false, it
                            will return immediately with whatever
                            response was received.
        kwargs              See the API options for the various opts
        """
        # All the option values in the kwargs should have integer values
        # so set them as such
        for key, val in list(kwargs.items()):
            try:
                kwargs[key] = int(val)
            except:
                # If we can't convert it, leave it as a string
                pass
        kwargs['username'] = username

        return self.call('collection', kwargs, wait)

    def get_forum_lists(self, fid, ftype='thing'):
        """
        Get a list of forums for a particular type.

        fid:int     Specifies the id of the type of database entry you want
                    the forum list for. This is the id that appears in the
                    address of the page when visiting a particular game in
                    the database.
        ftype:str   The forum list type. Default: thing
        """
        if ftype not in self.forum_list_types:
            raise InvalidInputError('Forum type must be either "thing" or '
                '"family"')
        d = {
            'id': int(fid),
            'type': ftype,
        }

        return self.call('forumlist', d)

    def get_forums(self, fid, page=1):
        """
        Get a list of threads in a particular forum

        fid:int     The ID of the forum to get the threads for
        page:int    The page of the returned list.  Page size is 50.  Threads
                    are sorted in order of most recent post
        """
        d = {
            'id': int(fid),
            'page': int(page),
        }

        return self.call('forum', d)

    def get_threads(self, tid, min_article_id=None, min_article_date=None,
            count=None, username=None):
        """
        Gets forum thread(s) for the given thread id(s).

        tid:int|list[int]       The thread id(s) to retrieve
        min_article_id:int      Filters results so that only articles >= to the
                                id are returned
        min_article_date:str    Filters results so only articles >= to the
                                date/datetime are returned.  Should be in the
                                format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
        count:int               Limits the number of articles returned to
                                "count" maximum
        username:str            *NOT CURRENTLY SUPPORTED*
        """
        if isinstance(tid, (list, tuple)):
            tid = ','.join([ str(i) for i in tid ])

        d = {
            'id': tid,
            'minarticledate': min_article_date,
            'username': username,
            'count': int(count) if count is not None else count,
            'minarticleid': int(min_article_id) if min_article_id is not None \
                else min_article_id,
        }

        return self.call('thread', d)

    def get_user(self, username, buddies=False, guilds=False, hot=False,
            top=False, domain='boardgame', page=1):
        """
        Get information about a user.

        username:str        The username to get the info about
        buddies:bool        Get buddies reports too. Default: False
        guilds:bool         Get guilds reports too. Default: False
        hot:bool            Include the user's hot 10 list. Default: False
        top:bool            Include the user's top 10 list. Default: False
        domain:str          Controls the domain for the user's hot/top 10
                            Default: boardgame
        page:int            The page of items to return.  Page size is 100
        """
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

    def get_guilds(self, gid, members=False, sort='username', page=1):
        """
        Gets the guild(s) for the given guild id(s).

        gid:int|list[int]   The guild id(s) to retrieve
        members:bool        Include the member roster in the results.
                            Default: False
        sort:str            How the results should be sorted when returned.
                            Default: username
        page:int            The page number to retrieve.  Page size is 25
        """
        if isinstance(gid, (list, tuple)):
            gid = ','.join([ str(i) for i in gid ])

        if sort not in self.guild_sorts:
            raise InvalidInputError('Guild sort types must be one of '
                '{}'.format(', '.join(self.guild_sorts)))

        d = {
            'id': gid,
            'members': int(members),
            'sort': sort,
            'page': int(page),
        }

        return self.call('guild', d)

    def get_plays(self, username=None, gid=None, play_type='thing',
            min_date=None, max_date=None, subtype='boardgame', page=1):
        """
        Gets the plays for a particular username, or game id and play type.
        The default play type is "thing" and you must specify either a 
        game id or a username.

        username:str        The BGG username to retrieve plays for
        gid:int             The ID of the game to get the plays for
        play_type:str       The type of item to retrieve. Default: thing
        min_date:str        The starting date for the plays to retrieve.
                            Should be in the form of YYYY-MM-DD
        max_date:str        The ending date for the plays to retrieve.
                            Should be in the form of YYYY-MM-DD
        subtype:str         The subtype to get plays for.  Default: boardgame
        page:int            The page to retrieve for this. Page size is 100
        """
        if play_type not in self.play_types:
            raise InvalidInputError('play_type must be one of {}'.format(
                ', '.join(self.play_types)))

        if subtype not in self.play_subtypes:
            raise InvalidInputError('play_subtype must be one of {}'.format(
                ', '.join(self.play_subtypes)))

        if username is None and gid is None:
            raise InvalidInputError('You must specify either a username or '
                'a game id (gid)')
        
        d = {
            'username': username,
            'id': int(gid) if gid is not None else gid,
            'type': play_type,
            'mindate': min_date,
            'maxdate': max_date,
            'subtype': subtype,
            'page': int(page),
        }

        return self.call('plays', d)

    def get_hotness(self, hot_type='boardgame'):
        """
        Gets the list of hot items by type.

        hot_type:str    Gets a list of hot items for the given type
        """
        if hot_type not in self.hot_types:
            raise InvalidInputError('hot_type must be one of {}'.format(
                ', '.join(self.hot_types)))

        d = {'type': hot_type}

        return self.call('hot', d)
