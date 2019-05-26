from PyQt5 import uic, QtWidgets
import sys
import ui.OptionsDialog as OptionsDialog
import ui.GameWidget as GameWidget
from PySide2.QtCore import Slot
from game_engine.Utils import Utils
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    """Cette classe implémente la fenêtre principale de l'application"""

    def __init__(self, gamesManager):
        super(MainWindow, self).__init__()
        uic.loadUi('UI/MainWindow.ui', self)

        # Initialisation des membres
        self.m_gamesManager = gamesManager
        self.optionDialog = OptionsDialog.OptionsDialog(gamesManager)

        # Connection des actions à leurs slots
        self.actionOptions.triggered.connect(self.onOptionDialog)
        self.actionExit.triggered.connect(self.onExit)
        self.actionNew_game.triggered.connect(self.onNewGame)


    # Appelé quand le menu Options est activé
    @Slot()
    def onOptionDialog(self):
        self.optionDialog.exec()

    # Appelé quand le menu 'Nouveau jeu' est activé
    @Slot()
    def onNewGame(self):
        isDicoValid, dicoContents, errorMessage = Utils.getDicoContents(self.m_gamesManager.options.pathToDicos, self.m_gamesManager.options.lettersCount)
        if isDicoValid:
            game = self.m_gamesManager.createNewGame(dicoContents)
            gw = GameWidget.GameWidget(game)
            self.mdiArea.addSubWindow(gw)
            gw.show()
            game.start()
        else:
            QtWidgets.QMessageBox.critical(self, 
                                           "Erreur dans Motus",
                                           "Le dictionnaire de mots de " + str(self.m_gamesManager.options.lettersCount) + " lettres est invalide:\n" + errorMessage)

    # Appelé quand le menu Quitter est activé
    @Slot()
    def onExit(self):
        sys.exit(0)
