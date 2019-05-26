from game_engine.Utils import Utils
from random import *
from PySide2.QtCore import QObject, Signal, Slot, QTimer
from enum import Enum

# Enumeration des status des lettres
class LetterPlacement(Enum):
    isWellPlaced = 0
    exists = 1
    doesNotExist = 2


class Game(QObject):
    """Cette classe contient l'algorithme de Motus"""

    def __init__(self, options, dico):
        super(Game, self).__init__()

        # Initialisation avec les paramètres
        self.m_options = options
        self.m_dico = dico

        # Initialisation des membres du jeu
        self.m_currentStep = -1     # L'index courant du jeu. Il sera incrémenté dés le démarrage du jeu
        self.m_isTimeOver = False   # Variable utilisée dans la fonction isGameOver()
        
        # Choix aléatoire du mot VALIDE à découvrir
        isWordValid = False
        while not isWordValid:
            self.m_wordToFind = Utils.getNormalizedToUpperCaseWord(dico[randint(0, len(dico) - 1)])
            isWordValid = Utils.isWordValid(self.m_wordToFind)

        print("Debug: Le mot à trouver est: " + self.m_wordToFind)

        # Création de la table de hachage des lettres contenues dans le mot
        # Il nous servira à déterminer si chaque lettre du mot joué est présente mais mal placée
        self.m_presentLettersSet = set()
        for letter in self.m_wordToFind:
            self.m_presentLettersSet.add(letter)

        print("Debug: Les lettres à trouver sont: " + str(self.m_presentLettersSet))

        # On retient la première lettre qui sera proposée au joueur
        self.m_firstLetter = str(self.m_wordToFind[0])

        # On crée le timer qui va appeler une fois toutes les 1000 ms (1 s) 
        # la fonction onOneSecondElapsed qui va controller le temps écoulé
        self.m_timer = QTimer()
        self.m_elapsedTime = 0
        self.m_timer.timeout.connect(self.onOneSecondElapsed)
        self.m_timer.start(1000)

    # --- Signaux

    # Ce signal sera emis au moment de donner la main au joueur
    # Son paramètre est une chaine de caractère contenant la première lettre
    proposeFirstLetterSignal = Signal(str)  
    
    # Ce signal sera emis juste après l'évaluation du mot joué
    # Paramètre 1: L'index du coup joué
    # Paramètre 2: Le mot joué
    # Paramètre 3: La liste du type de placement de chaque lettre du mot (LetterPlacement)
    playedSignal = Signal(int, str, list)   

    # Ce signal est émis chaque seconde. Son paramètre est le nombre de secondes écoulées
    progressSignal = Signal(int)            

    # Ce signal est émis à la fin du jeu, soit parce que le temps est écoulé,
    # soit parce que le nombre maximu de coups a été atteint, soit parce que le mot a été trouvé
    # Son paramètre est True si le mot est trouvé, False sinon
    gameOverSignal = Signal(bool)           

    # --- Slots

    # Cette méthode est appelée toutes les secondes
    @Slot()
    def onOneSecondElapsed(self):
        # On incrémente le nombre de secondes écoulées
        self.m_elapsedTime = self.m_elapsedTime + 1   
        
        # On informe les objets connectés à ce signal 
        # (par exemple une QProgressBar) de l'avancement
        self.progressSignal.emit(self.m_elapsedTime)        

        # Si on a dépassé le temps imparti:
        if self.m_elapsedTime >= self.m_options.duration:   
            # On spécifie que le temps est terminé, et donc que le jeu est terminé pour cette raison
            self.m_isTimeOver = True                        
 
            # On arrète le timer
            self.m_timer.stop()                             
           
            # On informe les objects connectés à ce signal que le jeu est fini non gagnant
            self.gameOverSignal.emit(False)                 

    # --- Propriétés

    # Permet d'accéder aux options depuis l'extérieur
    @property
    def options(self):
        return self.m_options

    # Permet d'accéder au dictionnaire depuis l'extérieur
    @property
    def dico(self):
        return self.m_dico

    # --- Méthodes
    
    # Cette méthode permet de démarrer le jeu
    def start(self):
        self.playNextStep()

    # Cette méthode joue le coup suivant
    def playNextStep(self):
        # On propose la première lettre aux objets connectés au signal proposeFirstLetterSignal
        self.proposeFirstLetterSignal.emit(self.m_firstLetter)

        # On incrémente l'index du jeu
        self.m_currentStep = self.m_currentStep + 1

    # Cette méthode est le point d'entrée pour jouer un mot
    def play(self, word):
        # On informe les objects connectés à ce signal de l'index du jeu, du mot joué 
        # et du résultat de l'analyse, lettre par lettre
        self.playedSignal.emit(self.m_currentStep, word, self.getResult(word))

        # Si le jeu n'est pas terminé, on joue le coup suivant
        if not self.isGameOver():
            self.playNextStep()
        else:
            self.gameOverSignal.emit(False)


    # --- Functions

    # Renvoie si un mot est valide ou pas
    def isWordValid(self, word):
        if len(word) < self.m_options.lettersCount:
            return False

        for letter in word:
            if letter < 'A' or letter > 'Z':
                return False

        return True


    # Le jeu est terminé si le temps est écoulé, ou qu'on atteint le nombre maximum d'éssais
    def isGameOver(self):
        return self.m_isTimeOver or self.m_currentStep >= self.m_options.m_maximumTriesCount - 1

    # Cette fonction analyse le mot joué pour renvoyer, lettre par lettre cette analyse
    def getResult(self, word):
        allGood = True
        l = []                          # Liste des analyses

        # On parcourt le mot avec son index
        for i in range(len(word)):

            # Si les lettres des 2 mots sont les mêmes
            if word[i] == self.m_wordToFind[i]:
                l.append(LetterPlacement.isWellPlaced)
            else:
                allGood = False # Toutes les lettres ne sont pas bien placées
                
                # Si la lettre se trouve dans la table de hachage qu'on a créée dans le constructeur
                if word[i] in self.m_presentLettersSet:
                    # La lettre existe, mais n'est pas bien placée
                    l.append(LetterPlacement.exists)
                else:
                    # Sinon, elle n'existe pas
                    l.append(LetterPlacement.doesNotExist)

        # Si toutes les lettres sont bien placées, le jeu est terminé
        if allGood:
            # On arrète le timer
            self.m_timer.stop()
            # Et on informe que je jeu est terminé gagnant
            self.gameOverSignal.emit(True)

        # On retourne enfin la liste des types de placement de lettres
        return l


