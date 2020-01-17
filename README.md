# emoji-parser
this Emoji Parser takes a string as input and extracts all emojis contained inside that string.  It returns a list of dictionaries. Each dictionary represents one emoji from that input-string.

# Usage with string-Objects
```python
import emojiParser


emojiParser = emojiParser(unicodeEmojiVersion=12.1)

emojiParser.parseStringObjet('this parser makes my life soo much easier ✌️ 👨🏼‍🦱 👩🏾‍🦰 😂')
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
                'text_string': '😂',
                'text_unicode': '1f602',
                'text_bytes': b'\xf0\x9f\x98\x82',
                'emoji_name': 'face with tears of joy',
                'group': 'Smileys & Emotion',
                'subgroup': 'face-smiling',
                'indices': [55]
            }
           ]
}
