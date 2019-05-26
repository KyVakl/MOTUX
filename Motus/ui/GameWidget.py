from PyQt5 import uic, QtWidgets, QtGui
from PySide2.QtCore import Slot, Qt
from PySide2.QtMultimedia import QSound
import ui.MotusTableWidget as MotusTableWidget
from game_engine.Game import LetterPlacement, Utils

class GameWidget(QtWidgets.QWidget):
    """Cette classe implémente l’IHM du jeu"""

    def __init__(self, game):
        super(GameWidget, self).__init__()
        uic.loadUi('UI/GameWidget.ui', self)

        self.m_game = game
        self.labelInfo.setText('Motus de ' + str(self.m_game.options.lettersCount) 
                               + " lettres. Nombre maximum d'éssais: " + str(self.m_game.options.maximumTriesCount)
                               + ". Nombre de mots possibles: " + str(len(game.dico) - 1))
        
        self.lineEditWord.setMaxLength(self.m_game.options.lettersCount)

        self.m_motusTableWidget = MotusTableWidget.MotusTableWidget(game)
        self.progressBar.setMaximum(game.options.duration)

        # Sons
        self.beepSound = QSound("data/sounds/beep-3.wav")
        self.newGameSound = QSound("data/sounds/nouveau_mot.wav")
        self.winSound = QSound("data/sounds/kultur0407.wav")
        self.lostSound = QSound("data/sounds/incorrect.wav")

        self.verticalLayoutGameComponents.addWidget(self.m_motusTableWidget)

        # Connections
        self.toolButtonPlayWord.clicked.connect(self.onPlay)
        self.lineEditWord.textChanged.connect(self.onLineEditTextChanged)

        self.m_game.proposeFirstLetterSignal.connect(self.onFirstLetterProposed)
        self.m_game.playedSignal.connect(self.onPlayed)
        self.m_game.progressSignal.connect(self.onDurationChanged)
        self.m_game.gameOverSignal.connect(self.onGameOver)

    # --- Slots    

    # Appelé quand le contenu du mot joué est modifié
    @Slot(str)
    def onLineEditTextChanged(self, word):
        self.lineEditWord.textChanged.disconnect(self.onLineEditTextChanged)
        w = Utils.getNormalizedToUpperCaseWord(word)
        if self.m_game.isWordValid(word):
            self.lineEditWord.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255, 255); } ")
        else:
            self.lineEditWord.setStyleSheet("QLineEdit { background-color: rgb(255, 0, 0, 127); } ")

        self.lineEditWord.setText(w)
        self.lineEditWord.textChanged.connect(self.onLineEditTextChanged)

    # Appelé quand un on clicque sur le bouton jouer 
    @Slot()
    def onPlay(self):
        self.m_game.play(self.lineEditWord.text())

    # Appelé quand la première lettre du mot est proposée par le jeu
    @Slot()
    def onFirstLetterProposed(self, firstLetter):
        self.lineEditWord.setText(firstLetter)
        self.newGameSound.play()

    # Appelé quand un essai a été validé par le jeu
    @Slot(int, str)
    def onPlayed(self, row, word, result):
        for column in range(len(word)):
            self.m_motusTableWidget.setLetter(row, column, str(word[column]), result[column])
    
    # Appelé quand le jeu signale une seconde écoulée
    @Slot(int)
    def onDurationChanged(self, duration):
        self.progressBar.setValue(duration)
        self.beepSound.play()

    # Appelé quand le jeu est terminé
    @Slot(bool)
    def onGameOver(self, isWinner):
        self.lineEditWord.setEnabled(False)
        self.toolButtonPlayWord.setEnabled(False)

        if isWinner:
            self.labelResult.setText("Gagné")
            self.winSound.play()
        else:
            self.labelResult.setText("Perdu")
            self.lostSound.play()
