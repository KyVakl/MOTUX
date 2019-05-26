import unicodedata

class Utils(object):
    """Cette classe contient des utilitaires généraux"""

    # Renvoie un mot en majuscules et sans accent
    @staticmethod
    def getNormalizedToUpperCaseWord(word):
        bytes = str(unicodedata.normalize('NFKD', word.upper()).encode('ASCII', 'ignore'))
        w = ''
        for i in range(2, len(bytes) - 1):
            w = w + bytes[i]
        return w;

    # Renvoie si un mot est valide ou pas
    @staticmethod
    def isWordValid(word):
        # On enlève les mots du type "L'OPERA"
        for letter in word:
            if letter < 'A' or letter > 'Z':
                return False
        
        return True


