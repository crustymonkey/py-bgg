
from libbgg.apibase import BGGBase
from libbgg.errors import InvalidInputError
from datetime import date

class BGG(BGGBase):
    def __init__(self, url_base='http://www.boardgamegeek.com', 
            path_base='xmlapi'):
        super(BGG, self).__init__(url_base, path_base)

    def search(self, search_str, exact=False):
        """
        Search for board games by string.  If exact is true, only exact
        matches will be returned
        
        search_str:str          The string to search for
        exact:bool              Match the string exactly
        """
        d = {'search': search_str, 'exact': int(exact)}

        return self.call('search', d)

    def get_game(self, game_ids=None, comments=False, comments_page=1,
            stats=False, historical=False, historical_start=None, 
            historical_end=None):
        """
        Gets info on a particular game or games.  game_ids can be either
        an integer id, a string id ("12345"), or an iterable of ids.

        game_ids:(str|int|list[int|str])    The id or ids to get info for
        comments:bool       Get user comments.  Can be paginated with
                            comments_page
        comments_page:int   The page of comments to retrieve
        stats:bool          Retrieve game stats
        historical:bool     Include historical game stats
        historical_start:datetime.date      The start date for historical stats
        historical_end:datetime.date        The end date for historical stats
        """
        if isinstance(game_ids, (str, int)):
            game_ids = [int(game_ids)]
        else:
            game_ids = [int(gid) for gid in game_ids]

        d = {'stats': int(stats)}

        if comments:
            # Set the comments options
            d['comments'] = 1
            d['comments_page'] = comments_page

        if historical:
            # Set the historical options
            d['historical'] = 1

            if isinstance(historical_start, date):
                d['from'] = str(historical_start)
            elif historical_start is not None:
                raise InvalidInputError('"historical_start" must be of type '
                    'datetime.date, not {}'.format(type(historical_start)))

            if isinstance(historical_end, date):
                d['to'] = str(historical_end)
            elif historical_end is not None:
                raise InvalidInputError('"historical_end" must be of type '
                    'datetime.date, not {}'.format(type(historical_end)))

        return self.call('boardgame/{}'.format(
            ','.join([str(gid) for gid in game_ids])), d)

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
        for key, val in kwargs.items():
            kwargs[key] = int(val)

        return self.call('collection/%s' % username, kwargs, wait)

    def get_thread_messages(self, thr_id, start=0, count=100, 
            username=None):
        """
        Gets messages from a forum/game thread.

        thr_id:int          The thread id
        start:int           The start article, increment this for pagination
        count:int           Number of messages to return, the default and
                            max are 100
        username:str        The username to filter for
        """
        thr_id = int(thr_id)
        d = {'start': int(start), 'count': int(count)}
        if d['count'] > 100:
            raise InvalidInputError('The maximum value for "count" is 100, and '
                'you requested {}'.format(count))
        if username is not None:
            d['username'] = username
        return self.call('thread/{}'.format(thr_id, d))

    def get_geeklist(self, list_id, comments=False):
        """
        Gets the geeklist given the specified id.

        list_id:int         The geeklist id
        comments:bool       If set to True, will also retrieve the comments
        """
        list_id = int(list_id)
        d = {'comments': int(comments)}
        return self.call('geeklist/{}'.format(list_id), d)
