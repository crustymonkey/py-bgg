# py-bgg #

A simple Board Game Geek (boardgamegeek.com) API library in Python.  
This mainly just handles the API calls and converts the XML to 
representative dict/list format

**0.3.0 has moved to Python3 ONLY**.  Python2 is dead, long live Python2.

## INSTALL ##

Installation is pretty easy.  You can just to the standard as root:

    tar -xvzf py-bgg-*.tar.gz
    cd py-bgg-*
    python setup.py install

You can also install directly using `pip`
    
    pip install py-bgg

## USAGE ##

This follows the BGG api pretty closely so this should be self-explanatory
with "pydoc libbgg" and the api definition at:

http://boardgamegeek.com/wiki/page/BGG_XML_API  
http://boardgamegeek.com/wiki/page/BGG_XML_API2

## BASIC TUTORIAL ##

This library will essentially just convert your calls into a URL and
subsequently return a dict/list tree of objects that are accessible via
standard object notation or dictionary style access

```python
#!/usr/bin/env python3

import json
from libbgg.apiv1 import BGG
# You can also use version 2 of the api:
from libbgg.apiv2 import BGG as BGG2

conn = BGG()

# Perform a search
results = conn.search('bruges')
print(json.dumps(results, indent=4, sort_keys=True))

# Print out a list of names that were returned
for game in results.boardgames.boardgame:
    print(game.name.TEXT)

# You can also access items as a dictionary
for game in results['boardgames']['boardgame']:
    print(game['name']['TEXT'])

# Get game info
results = conn.get_game(136888 , stats=True)
print(json.dumps(results, indent=4, sort_keys=True))

# V2
conn2 = BGG2()
results = conn2.boardgame(136888, stats=True)
print(json.dumps(results, indent=4, sort_keys=True))
```
