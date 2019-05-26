import pickle
from common.Parameters import Parameters

from common.Utils import Utils as BaseUtils

class Utils(BaseUtils):
    """Cette classe contient des utilitaires spécifiques au jeu"""

    # Renvoie le chemin complet vers les dictionnaires
    @staticmethod
    def getDicoFullPath(path, lettersCount):
        return path + "\\" + str(lettersCount) + ".dico"

    # Lit et renvoie le contenu d'un dictionnaire
    @staticmethod
    def getDicoContents(path, lettersCount):
        dicoPath = Utils.getDicoFullPath(path, lettersCount)
        try:
            with open(dicoPath, 'rb') as pickle_file:
                return True, pickle.load(pickle_file), ''
        except Exception as error:
            message = "Le chargement du dictionnaire '" + dicoPath + "' a échoué, car \n" + str(error.args)
            print('Erreur: ' + message)
            return False, [], message

    # Renvoie si le dictionnaire est valide ou pas
    @staticmethod
    def isDicoValid(path, lettersCount):
        isValid, dicoContents, errorMessage = Utils.getDicoContents(path, lettersCount)

        if not isValid:
            return False, errorMessage

        if len(dicoContents) < Parameters.minimumWordsInDico():
            message = "Le dictionnaire '" + Utils.getDicoFullPath(path, lettersCount) + "' ne contient que " + str(len(dicoContents)) + " mots; le minimum est " + str(Parameters.minimumWordsInDico())
            print('Erreur: ' + message)
            return False, message

        return True, ''



