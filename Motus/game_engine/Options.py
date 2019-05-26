import os

class Options(object):
    """Cette classe contient toutes les options du jeu"""

    def __init__(self):
        self.m_pathToDicos = os.getcwd() + '\\data\\sub_dicos'
        self.m_lettersCount = 7
        self.m_maximumTriesCount = 10
        self.m_duration = 120 # secondes
        self.m_letterWellPlacedColor = 255, 0, 0    # Rouge
        self.m_letterExistsColor = 255, 255, 0      # Jaune
        self.m_letterDoesNotExistColor = 0, 0, 255  # Bleu

    # Propriétés

    # Chemin vers les dictionnaires
    @property
    def pathToDicos(self):
        return self.m_pathToDicos

    @pathToDicos.setter
    def pathToDicos(self, value):
        self.m_pathToDicos = value

    # Nombre de lettres du mot
    @property
    def lettersCount(self):
        return self.m_lettersCount

    @lettersCount.setter
    def lettersCount(self, value):
        self.m_lettersCount = value

    # Durée maximale du jeu
    @property
    def duration(self):
        return self.m_duration

    @duration.setter
    def duration(self, value):
        self.m_duration = value

    # Nombre maximum d'essais
    @property
    def maximumTriesCount(self):
        return self.m_maximumTriesCount

    @maximumTriesCount.setter
    def maximumTriesCount(self, value):
        self.m_maximumTriesCount = value

    # Couleur des lettres bien placées
    @property
    def letterPlacementWellPlacedColor(self):
        return self.m_letterWellPlacedColor

    @letterPlacementWellPlacedColor.setter
    def letterPlacementWellPlacedColor(self, value):
        self.m_letterWellPlacedColor = value

    # Couleur des lettres existantes
    @property
    def letterExistsColor(self):
        return self.m_letterExistsColor

    @letterExistsColor.setter
    def letterExistsColor(self, value):
        self.m_letterExistsColor = value

    # Couleur des lettres inexistantes
    @property
    def letterDoesNotExistColor(self):
        return self.m_letterDoesNotExistColor

    @letterDoesNotExistColor.setter
    def letterDoesNotExistColor(self, value):
        self.m_letterDoesNotExistColor = value


