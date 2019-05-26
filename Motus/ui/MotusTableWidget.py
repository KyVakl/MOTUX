from PyQt5 import uic, QtWidgets, QtGui
from PySide2.QtCore import Slot, Qt
from game_engine.Game import LetterPlacement

class MotusTableWidget(QtWidgets.QTableWidget):
    """Cette classe implémente l'IHM de la grille de mots"""

    def __init__(self, game):
        super(MotusTableWidget, self).__init__()

        self.m_game = game
        self.m_lettersColor = [self.m_game.options.letterPlacementWellPlacedColor, 
                               self.m_game.options.letterExistsColor, 
                               self.m_game.options.letterDoesNotExistColor ]

        self.setColumnCount(self.m_game.options.lettersCount)
        self.setRowCount(self.m_game.options.maximumTriesCount)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        for column in range(self.m_game.options.lettersCount):
            self.setColumnWidth(column, self.rowHeight(0)) # Les cellules seront carrées
            for row in range(self.m_game.options.maximumTriesCount):
                self.setLetter(row, column, "", LetterPlacement.doesNotExist)

    # Méthodes

    # Cette méthode place une lettre dans la grille et assigne la couleur en fonction de son placement
    def setLetter(self, row, column, letter, letterPlacement):
        cell = QtWidgets.QTableWidgetItem()
        cell.setTextAlignment(Qt.AlignCenter)
        cell.setText(letter)
        self.setItem(row, column, cell)
        cell.setBackground(QtGui.QColor(
            self.m_lettersColor[letterPlacement.value][0],
            self.m_lettersColor[letterPlacement.value][1],
            self.m_lettersColor[letterPlacement.value][2]
            ))
