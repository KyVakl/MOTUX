import game_engine.Options as Options
import game_engine.Game as Game

class GamesManager(object):
    """Cette classe est destinée à créer un jeu"""

    def __init__(self):
        self.m_minimumWordsInDico = 3
        self.m_options = Options.Options()

    # --- Propriétés

    # Options
    @property
    def options(self):
        return self.m_options

    @options.setter
    def options(self, value):
        self.m_options = value

    # Méthodes

    # Création d'un jeu
    def createNewGame(self, dico):
        return Game.Game(self.m_options, dico)