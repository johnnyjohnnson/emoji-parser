# -*- coding: utf-8 -*-
"""
@author: https://github.com/johnnyjohnnson
"""


import json
import re
import requests
import urllib.parse


class emojiParser():
    
    def __init__(self, unicodeEmojiVersion='latest'):#12.1):
        """
        input ist uniCodeEmojiVersion entweder als string 'latest'
        --> dann zieht er sich automatisch die aktuellste Version
        oder du gibst eine emojiVersion als float ein mit einer Dezimalstelle, zB 12.1
        --> dann lädt er die spezifizierte Version runter
        """
        
        def loadEmojiTable():
            try:
                return open('emoji_data_V{}.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='br')
            except FileNotFoundError:
                downloadEmojiTable()
                return open('emoji_data_V{}.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='br')
        
        def loadEmojiKeyboard():
            try:
                return open('emoji_Keyboard_V{}.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='br')
            except FileNotFoundError:
                downloadEmojiKeyboard()
                return open('emoji_Keyboard_V{}.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='br')
        
        def loadTableList():
            """
            Lädt die Datei von FP und konvertiert die strings in der Datei, welche ein Emoji als
            DezimalZahl repräsentieren, in Integers um.
            Wenn die Liste nicht existieren sollte, wird sie erzeugt.
            """
            
            def _loadAndConvertToList():
                """
                """
                file = open('emoji_data_V{}_IntegerList.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='r')
                #
                CODE_POINTS = file.readlines()
                for index in range(len(CODE_POINTS)):
                    CODE_POINTS[index] = int(CODE_POINTS[index])
                file.close()
                return CODE_POINTS
            
            try:
                CODE_POINTS = _loadAndConvertToList()
            except FileNotFoundError:
                convertEmojiTableIntoIntegerList()
                CODE_POINTS = _loadAndConvertToList()
            return CODE_POINTS
        
        def loadKeyboardDictionary():
            """
            Lädt die Datei von FP und konvertiert die strings in der Datei, welche ein Emoji als
            DezimalZahl repräsentieren, in Integers um.
            Wenn die Liste nicht existieren sollte, wird sie erzeugt.
            """
            def _loadAndConvertToDictionary():
                """
                """
                with open('emoji_Keyboard_V{}_Dictionary.json'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='r') as file:
                    return json.load(file)
            
            try:
                KEYBOARD_EMOJIS = _loadAndConvertToDictionary()
            except FileNotFoundError:
                convertEmojiKeyboardIntoDictionary()
                KEYBOARD_EMOJIS = _loadAndConvertToDictionary()
            return KEYBOARD_EMOJIS
        
        def downloadEmojiTable():
            """
            input ist die Unicode-Version für welche die emoji-data.txt Datei heruntergeladen werden soll
            
            returned wird nichts, geladene Datei wird auf Festplatte abgespeichert
            """
            
            res = requests.get(
                    'https://unicode.org/Public/emoji/{}/emoji-data.txt'.format(self.unicodeEmojiVersion)
                    )
            
            if res.status_code == 200:
                #save successfully downloaded data to disk
                with open('emoji_data_V{}.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='bw') as file:
                    file.write(res.content)
            elif res.status_code == 404:
                print("404-Error... the requested url doesn't exist. Maybe you are trying to use "
                      "an Emoji-Version that doesn't exist.")
            else:
                print('{}-Error...'.format(res.status_code))
        
        def downloadEmojiKeyboard():
            """
            input ist die Unicode-Version für welche die emoji-test.txt Datei heruntergeladen werden soll
            
            returned wird nichts, geladene Datei wird auf Festplatte abgespeichert
            """
            
            res = requests.get(
                    'https://unicode.org/Public/emoji/{}/emoji-test.txt'.format(self.unicodeEmojiVersion)
                    )
            
            if res.status_code == 200:
                #save successfully downloaded data to disk
                with open('emoji_Keyboard_V{}.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='bw') as file:
                    file.write(res.content)
            elif res.status_code == 404:
                print("404-Error... the requested url doesn't exist. Maybe you are trying to use "
                      "an Emoji-Version that doesn't exist.")
            else:
                print('{}-Error...'.format(res.status_code))
        
        def convertEmojiTableIntoIntegerList():
            """
            input ist die Unicode-Version für welche die emoji-data.txt Datei konvertiert werden soll
            
            returned wird nichts, aber dafür eine neue txt-Datei erzeugt, welche nur Integers enthält
            diese Integers repräsentieren den Dezimal-Wert eines Emojis
            """
            
            try:
                file = loadEmojiTable()
            except FileNotFoundError:
                downloadEmojiTable()
                file = loadEmojiTable()
                
            zeilenListe = file.readlines()
            self.CODE_POINTS = list()
            
            for line in zeilenListe:
                #line = b'1F249..1F24F  ; Extended_Pictographic# E0.0   [7] ...'
                #deswegen decodieren() und am Semikolon splitten
                line = line.decode().split(';')
                #nur der erste Teil der entstandenen Liste ist interessant
                codePoint = line[0]
                if codePoint.startswith('#') or codePoint.startswith('\n'):
                    #das hier sortiert Bullshit-Zeilen aus
                    continue
                else:
                    #"0023        " --> ganz viele Whitespaces --> rstrip() löscht die weg
                    codePoint = codePoint.rstrip()
                    #es handelt sich hier um hexZahlen, wenn sie sehr niedrige Werte haben
                    #sehen sie am Anfang so aus "0023". gemeint ist aber eigentlich "23"
                    #deswegen -->lstrip('0')
                    codePoint = codePoint.lstrip('0')
                    #codePoint = '23' oder '1F21A', oder '1F232..1F23A'
                    #deswegen muss codePoint nochmal wegen der '..' gesplittet werden
                    #codePoint = ['23'] oder ['1F232', '1F23A']
                    codePoint = codePoint.split('..')
                    if len(codePoint) > 1:
                        #dann war codePoint.split('..') erfolgreich und es resultiert ein StartWert
                        # in der Liste, z.B. '30' und ein EndWert z.B. '0039'
                        # Endwert nochmal .lstrip('0') machen, damit die Nullen weggehen
                        codePoint[1] = codePoint[1].lstrip('0')
                        #die beiden durch '..' getrennten hexWerte werden durch die folgende
                        #Schleife mit aufgefüllt. gleichzeitig erfolgt Umwandlung in Dezimal-Werte
                        missingCodePoints = list()
                        start = eval('0x' + codePoint[0])
                        ende  = eval('0x' + codePoint[1])
                        #
                        for value in range(start, ende +1, 1):
                            missingCodePoints.append(value)
                        #erzeugte Liste in die Finale self.CODE_POINTS-Liste extenden
                        self.CODE_POINTS.extend(missingCodePoints)
                    else:
                        #dann musste die Variable codePoint nicht gesplittet werden
                        #codePoint = ['23'] --> '0x' davor und mit eval in eine Dezimalzahl verwandeln
                        codePoint = eval('0x' + codePoint[0])
                        self.CODE_POINTS.append(codePoint)
            #
            file.close()
            #save the converted emoji-data-IntegerList to disk
            with open('emoji_data_V{}_IntegerList.txt'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='w') as file:
                for codePoint in self.CODE_POINTS:
                    file.write(str(codePoint) + '\n')
        
        def convertEmojiKeyboardIntoDictionary():
            """
            input ist die Unicode-Version für welche die emoji-test.txt Datei konvertiert werden soll
            
            returned wird nichts, aber dafür eine neue txt-Datei erzeugt, welche ein Dictionary
            erzeugt, in dem die Keys die Unicode-"code-points" sind.
            jeder Key enthält eine liste. erstes Element der Liste ist die Kategorie des Emojis,
            zweites Element die Bezeichnung/Beschreibung des Emojis
            {'1F468 1F3FF 200D 1F9B0': ['person', 'man: dark skin tone, red hair']}
            """
            
            try:
                file = loadEmojiKeyboard()
            except FileNotFoundError:
                downloadEmojiKeyboard()
                file = loadEmojiKeyboard()
                
            zeilenListe = file.readlines()
            self.KEYBOARD_EMOJIS = {}
            for line in zeilenListe:
                #line ist im ByteFormat, deswegen durch .decode() in einen String umwandeln
                line = line.decode()
                #das erste Element (1f600) der Liste ist der HexCode, wird der neue Key fürs self.KEYBOARD_EMOJIS
                if line.startswith('# group'):
                    line = line.split(':')
                    #line = ['# group', ' Smileys & Emotion\n']
                    groupName = line[-1]
                    groupName = groupName.lstrip().rstrip()
                elif line.startswith('# subgroup'):
                    line = line.split(':')
                    #line = ['# subgroup' ' face-smiling\n']
                    subgroupName = line[-1]
                    subgroupName = subgroupName.lstrip().rstrip()
                elif line.startswith('#') or line.startswith('\n'):
                    #das hier sortiert Bullshit-Zeilen aus
                    continue
                else:
                    #es handelt sich um eine Zeile gefüllt mit Emoji-Informationen, z.B.:
                    #line = '1F600   ; fully-qualified     # 😀 E2.0 grinning face'
                    #erstmal am Semikolon splitten
                    line = line.split(';')
                    codePoint = line[0]
                    # + Whitespaces links und rechts strippen() und den UnicodeHexCode lowercasen
                    codePoint = codePoint.lstrip().rstrip().lower()
                    #jetzt noch den emojiNamen extrahieren
                    emojiName = line[1]
                    #emojiname = ' fully-qualified     # 😀 E2.0 grinning face'
                    #bei E2.0 splitten
                    emojiName = re.split(r'[E][0-9]+\.[0-9]', emojiName, re.I)
                    emojiName = emojiName[-1].lstrip().rstrip()
                    #updaten des self.KEYBOARD_EMOJIS-Dictionary
                    self.KEYBOARD_EMOJIS.update(
                            { codePoint: {'emoji_name': emojiName, 'group': groupName, 'subgroup': subgroupName} }
                            )
            #
            file.close()
            #save the converted emoji-Keyboard-data to disk
            with open('emoji_Keyboard_V{}_Dictionary.json'.format(str(self.unicodeEmojiVersion).replace('.', 'p')), mode='w') as file:
                json.dump(self.KEYBOARD_EMOJIS, file)

        
        
        if unicodeEmojiVersion == 'latest':
            res = requests.get('https://unicode.org/Public/emoji/latest')
            #url = 'https://unicode.org/Public/emoji/12.1'
            url = res.url
            #path = '/Public/emoji/12.1'
            path = urllib.parse.urlparse(url).path
            path = path.replace('/', ' ')
            #path = ['Public', 'emoji', '12.1']
            path = path.split()
            #self.unicodeEmojiVersion = 12.1
            self.unicodeEmojiVersion = eval(path[-1])
            print('latest emojiVersion is {}'.format(self.unicodeEmojiVersion))
        else:
            self.unicodeEmojiVersion = unicodeEmojiVersion
        
        self.CODE_POINTS     = loadTableList()
        self.KEYBOARD_EMOJIS = loadKeyboardDictionary()
        self.appendable = False
        
        
#______________________________________________________________________________
    
    
    def _parseForEmojis(self, potentialEmojiBytes, Index):
        """
        input ist potentialEmojiBytes als ein bytes-Object und Index als eine integer-Zahl
        (Index gibt die Position des potentiellen Emojis im Text an)
        """
        
        def returnEmojiAsDecimalNumber(potentialEmoji):
            """
            input ist ein potentielles Emoji in Byte-Form --> b'\xf0\x9f\x92\x91'
            returned wird der DezimalWert dieses übergebenen Byte-Strings
            """
            #potentialEmoji liegt jetzt in bytes-Form vor, z.B. b'\xf0\x9f\x92\x91'
            #umwandeln in eine Liste, z.B. ['0b11110000', '0b10011111', '0b10010010', '0b10010001']
            arrayOfBinBytes = [ bin(decByte) for decByte in potentialEmoji ]
            #
            binaryString = '0b'
            for binByte in arrayOfBinBytes:
                #binByte[2: ] = z.B. '11110000' --> alle 1en von links weghauen
                binByte = binByte[2: ].lstrip('1')
                #ergibt '0000', die erste Stelle des neuen Strings ignorieren -->'000'
                binaryString += binByte[1: ]
            #binaryString ist am Ende sowas zB: '0b000011111010010010001'
            #mit eval() in einen DezimalWert umwandeln
            return eval(binaryString)
        
        def itsAnEmoji(potentialEmoji):
            """
            input ist ein potentielles Emoji in Form eines byte-Strings
            1) Umrechnen in eine DezimalZahl
            2) lookup machen, ob es sich bei dem Dezimalwert um einen Wert handelt, der
                in der Emoji-Chart-Table drin ist
            """
            if potentialEmoji in self.CODE_POINTS:
                return True
            else:
                return False
            
        def __updateWithEmojiKeyboardData(potentialEmojiUnicode):
            """
            """
            self.partialEntityDict['emojis'][-1].update(
                    self.KEYBOARD_EMOJIS[potentialEmojiUnicode]
                    )
        
        def __updateWithPlaceholders():
            """
            """
            self.partialEntityDict['emojis'][-1].update(
                    {'emoji_name': 'unknown', 'group': 'unknown', 'subgroup': 'unknown'}
                    )
        
        def _appendToExistingEmoji(potentialEmojiBytes, potentialEmojiUnicode, Index):
            """
            input ist potentialEmojiBytes als ein bytes-Object, Index als eine integer-Zahl
            (Index gibt die Position des potentiellen Emojis im Text an) und
            potentialEmojiUnicode der hex-Wert des CodePoints des potentiellen Emojis
            (Achtung: ist ein String)
            """
            #emoji_name/group/subgroup aktualisieren
            #potentialEmojiUnicode = zB '0x1f600'
            potentialEmojiUnicode = potentialEmojiUnicode[2:]
            try:
                if potentialEmojiUnicode == '200d':
                    #wenn es sich um einen ZWJ handelt, dann die Funktion weiter durchlaufen.
                    pass
                else:
                    __updateWithEmojiKeyboardData(
                            #die nächste Zeile ist der alte Unicode-Wert + das neue potentielle Emoji/ZWJ/VS
                            self.partialEntityDict['emojis'][-1]['text_unicode'] + ' ' + potentialEmojiUnicode
                            )
            except KeyError:
                #der Key im self.KEYBOARD_EMOJIS existiert nicht, das bedeutet der Tweet enthält
                #emojis, die so nicht existieren, zB das hier würde als EIN Emoji erkannt,
                #was aber nicht existiert: 🖋️🙂 aber durch den VS nach dem Pen dieses Verhalten auslöst  
                #also muss ein neues Emoji in das self.partialEntityDict eingefügt werden
                _createNewEmojiEntity(potentialEmojiBytes, '0x' + potentialEmojiUnicode, Index)
            else:
                self.partialEntityDict['emojis'][-1]['text_bytes']   += potentialEmojiBytes
                self.partialEntityDict['emojis'][-1]['text_string']  += potentialEmojiBytes.decode()
                self.partialEntityDict['emojis'][-1]['text_unicode'] += ' ' + potentialEmojiUnicode
                #
                #Indizes aktualisieren
                try:
                    #versuchen das zweite 'indices'-Element der Liste mit dem richtigen 
                    #Index zu versehen. 'indices'-Liste hat ein start und ein stop Element
                    self.partialEntityDict['emojis'][-1]['indices'][1] = Index
                except IndexError:
                    #wenn die Liste aber bislang nur 1 Element lang ist wird ein IndexError kommen
                    self.partialEntityDict['emojis'][-1]['indices'].append(Index)
        
        def _createNewEmojiEntity(potentialEmojiBytes, potentialEmojiUnicode, Index):
            """
            input ist potentialEmojiBytes als ein bytes-Object, Index als eine integer-Zahl
            (Index gibt die Position des potentiellen Emojis im Text an) und
            potentialEmojiUnicode der hex-Wert des CodePoints des potentiellen Emojis
            (Achtung: ist ein String)
            """
            #
            potentialEmojiUnicode = potentialEmojiUnicode[2:]
            self.partialEntityDict['emojis'].append(
                    {
                            'text_bytes'  : potentialEmojiBytes,
                            'text_string' : potentialEmojiBytes.decode(),
                            'text_unicode': potentialEmojiUnicode,
                            'indices'     : [Index]
                            }
                    )
            #emoji_name/group/subgroup hinzufügen
            try:
                __updateWithEmojiKeyboardData(potentialEmojiUnicode)
            except KeyError:
                #der Key im self.KEYBOARD_EMOJIS existiert nicht, also erstmal Platzhalter einfügen
                __updateWithPlaceholders()
                #wenn es sich aber um ein Emoji der subgroup: country-flag handelt, z.B. '🇩' dann
                #wird definitiv ein weiterer Buchstabe kommen, z.B. '🇩🇪'deswegen appendable auf True setzen
                self.appendable = True
        #
        decimalValue = returnEmojiAsDecimalNumber(potentialEmojiBytes)
        #
        if itsAnEmoji(decimalValue):
            #
            if 0x1f3fb <= decimalValue <= 0x1f3ff:
                #wenn sich der Wert des potentiellen Emojis zwischen diesen beiden hex-Werten
                #befindet, dann handelt es sich um einen Fitzpatrickschen Farbmodifier
                #an den Vorgänger-Emoji appenden
                _appendToExistingEmoji(potentialEmojiBytes, hex(decimalValue), Index)
                self.appendable = False
                
            elif decimalValue == 0x200d:
                #wenn der Wert des potentiellen Emojis genau 0x200d (--> b'\xe2\x80\x8d') ist,
                #dann handelt es sich um einen "ZWJ" (Zero Width Join).
                #Verbindet ein Byte links und rechts miteinander -->self.appendable muss true bleiben
                _appendToExistingEmoji(potentialEmojiBytes, hex(decimalValue), Index)
                self.appendable = True
                
            elif decimalValue == 0xfe0f:
                #wenn der Wert des potentiellen Emojis genau 0xfe0f (--> b'\xef\xb8\x8f') ist,
                #dann handelt es sich um einen "VS" (Variational Selector).
                #Verbindet ein Byte links und rechts miteinander -->self.appendable muss true bleiben
                _appendToExistingEmoji(potentialEmojiBytes, hex(decimalValue), Index)
                self.appendable = True
                
            else:
                #es handelt sich um ein tatsächliches Emoji, evtl. muss zusammengesetzt werden
                if self.appendable:
                    #wenn self.appendable noch true ist, dann sollen mehrere Emojis zusammengesetzt werden
                    #zB ein FamilienEmoji aus mehreren Frau-, Mann-, Kind-Emojis
                    _appendToExistingEmoji(potentialEmojiBytes, hex(decimalValue), Index)
                    self.appendable = False
                else:
                    #dann ein neues eigenständiges Emoji im emojiDict aufmachen
                    _createNewEmojiEntity(potentialEmojiBytes, hex(decimalValue), Index)
        
    def parseStringObject(self, string):
        """
        input is a string
        der wird durchgewuselt nach Emojis
        
        returned wird ein Dictionary im Stile eines entity-Objects was sich nahtlos
        in die Tweet-Objects einfügt, die man bei Twitter runterlädt
        """
        
        self.partialEntityDict = {'emojis': []}
        
        Index = 0
        for character in string:
            potentialEmoji = character.encode()
            if len(potentialEmoji) >= 3:
                self._parseForEmojis(potentialEmoji, Index)
            else:
                self.appendable = False
            Index += 1
        return self.partialEntityDict
        
    def parseTweetObject(self, tweetObject):
        """
        """
        if isinstance(tweetObject, dict):
            try:
                self.parseStringObject(tweetObject['full_text'])
            except KeyError:
                try:
                    self.parseStringObject(tweetObject['text'])
                except KeyError:
                    raise TypeError("tweet-Object doesn't contain a 'text' or 'full_text' field which is required")
        else:
            raise TypeError("tweet-Object is supposed to be of type Dictionary "
                            "but is of type {}".format(type(tweetObject)))
        #
        tweetObject['entities'].update(self.partialEntityDict)
        return tweetObject





if __name__ == '__main__':
    
    
    emojiParser = emojiParser(unicodeEmojiVersion='latest')
    
    
    emojisInString = emojiParser.parseStringObject(
            'this parser extracts emojis out of strings ✌️ 👨🏼‍🦱 👩🏾‍🦰       '
            )
    
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
    emojiParser.parseTweetObject(elonsTweet)
    
    
    
    
    
    
    