# emoji-parser
this Emoji Parser takes a string or a Tweet-object as input and extracts all emojis contained inside that string/Tweet. It returns a dictionary with a list of dictionaries. Each dictionary of that list represents one emoji from that input-string or Tweet.

# Usage with string-Objects
```python
from emojiParserModul import emojiParser

emojiParser = emojiParser()
#it defaults to the latest Emoji-Unicode-Version as of right now --> 13.0
emojiParser.parseStringObject('this parser extracts emojis out of strings ✌️ 👨🏼‍🦱 👩🏾‍🦰 😂')
```

## it returns the following dictionary:
```python
{'emojis': [
            #1st emoji as a dictionary
            {
                'text_string' : '✌️',
                'text_unicode': '270c fe0f',                
                'text_bytes'  : b'\xe2\x9c\x8c\xef\xb8\x8f',
                'emoji_name'  : 'victory hand',
                'group'       : 'People & Body',
                'subgroup'    : 'hand-fingers-partial',
                'indices'     : [42, 43]
            },
             
            #2nd emoji as a dictionary
            {
                'text_string' : '👨🏼‍🦱',
                'text_unicode': '1f468 1f3fc 200d 1f9b1',
                'text_bytes'  : b'\xf0\x9f\x91\xa8\xf0\x9f\x8f\xbc\xe2\x80\x8d\xf0\x9f\xa6\xb1',
                'emoji_name'  : 'man: medium-light skin tone, curly hair',
                'group'       : 'People & Body',
                'subgroup'    : 'person',
                'indices'     : [45, 48]
            },
            
            #3rd emoji as a dictionary
            {
                'text_string' : '👩🏾‍🦰',
                'text_unicode': '1f469 1f3fe 200d 1f9b0',
                'text_bytes'  : b'\xf0\x9f\x91\xa9\xf0\x9f\x8f\xbe\xe2\x80\x8d\xf0\x9f\xa6\xb0',
                'emoji_name'  : 'woman: medium-dark skin tone, red hair',
                'group'       : 'People & Body',
                'subgroup'    : 'person',
                'indices'     : [50, 53]
            },
            
            #4th emoji as a dictionary
            {
                'text_string' : '😂',
                'text_unicode': '1f602',
                'text_bytes'  : b'\xf0\x9f\x98\x82',
                'emoji_name'  : 'face with tears of joy',
                'group'       : 'Smileys & Emotion',
                'subgroup'    : 'face-smiling',
                'indices'     : [55]
            }
           ]
}
```
# Usage with Tweet-Objects
```python
from emojiParserModul import emojiParser

elonsTweet = {
 'created_at': 'Fri Jan 10 09:57:08 +0000 2020',
 'id': 1215573277726273536,
 'id_str': '1215573277726273536',
 'full_text': '🎶 Toss a coin to ur Witcher 🎶',
 'truncated': False,
 'display_text_range': [0, 29],
 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': []},
 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
 'in_reply_to_status_id': None,
 'in_reply_to_status_id_str': None,
 'in_reply_to_user_id': None,
 'in_reply_to_user_id_str': None,
 'in_reply_to_screen_name': None,
 'user': {'id': 44196397, 'id_str': '44196397'},
 'geo': None,
 'coordinates': None,
 'place': None,
 'contributors': None,
 'is_quote_status': False,
 'retweet_count': 29090,
 'favorite_count': 216912,
 'favorited': False,
 'retweeted': False,
 'lang': 'en'
 }


emojiParser = emojiParser() 
#it defaults to the latest Emoji-Unicode-Version as of right now --> 13.0
emojiParser.parseTweetObject(elonsTweet)
```

## it returns a modified version of the Tweet-Object:
the modification is an update of the 'entities'-dictionary inside the Tweet-Object "elonsTweet". Since emojis could be viewed as some kind of entity, the 'entities'-dictionary gets updated by inserting an 'emojis'-field. This newly inserted 'emojis'-field contains every single emoji contained in that Tweet which was passed to the parseTweetObject-method.
```python

#now elonsTweet looks like this:

elonsTweet = {
 'created_at': 'Fri Jan 10 09:57:08 +0000 2020',
 'id': 1215573277726273536,
 'id_str': '1215573277726273536',
 'full_text': '🎶 Toss a coin to ur Witcher 🎶',
 'truncated': False,
 'display_text_range': [0, 29],
 'entities': {
            'hashtags': [],
            'symbols': [],
            'user_mentions': [],
            'urls': [],
            #this is the inserted 'emojis'-field into the 'entities'-dictionary
            'emojis': [
                        #1st emoji as a dictionary
                        {
                        'text_string' : '🎶',
                        'text_unicode': '1f3b6',
                        'text_bytes'  : b'\xf0\x9f\x8e\xb6',
                        'emoji_name'  : 'musical notes',
                        'group'       : 'Objects',
                        'subgroup'    : 'music',
                        'indices'     : [0],
                        },
                        
                        #2nd emoji as a dictionary
                        {
                        'text_string' : '🎶',
                        'text_unicode': '1f3b6',
                        'text_bytes'  : b'\xf0\x9f\x8e\xb6',
                        'emoji_name'  : 'musical notes',
                        'group'       : 'Objects',
                        'subgroup'    : 'music',
                        'indices'     : [28]
                        }
                      ]
             },
 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
 ...
 }
