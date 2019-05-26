import sys
from PyQt5 import uic, QtWidgets
from PySide2.QtCore import Slot
from game_engine.Utils import Utils
from common.Parameters import Parameters
 
class OptionsDialog(QtWidgets.QDialog):
    """Cette classe implémente l'IHM de la boite de dialogue d'options"""
    def __init__(self, gamesManager):
        super(OptionsDialog, self).__init__()
        uic.loadUi('UI/OptionsDialog.ui', self)
        self.m_gamesManager = gamesManager

        # Initialisations
        self.spinBoxLettersCount.setMinimum(Parameters.minimumWordsInDico())
        self.spinBoxLettersCount.setValue(self.m_gamesManager.options.lettersCount)
        self.spinBoxDuration.setValue(self.m_gamesManager.options.duration)
        self.spinBoxMaxTriesCount.setValue(self.m_gamesManager.options.maximumTriesCount)
        self.lineEditDicosPath.setText(self.m_gamesManager.options.pathToDicos)

        # Connections
        self.buttonBox.accepted.connect(self.onApplyNewValues)
        self.buttonBox.rejected.connect(self.onCancel)
        self.spinBoxLettersCount.valueChanged.connect(self.onLettersCountChanged)
    
    # Slots    

    # Appelé quand le nombre de lettres a changé
    @Slot()
    def onLettersCountChanged(self, count):
        isDicoValid, errorMessage = Utils.isDicoValid(self.lineEditDicosPath.text(), self.spinBoxLettersCount.value())
        if isDicoValid:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
            self.labelStatus.setText("")
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
            self.labelStatus.setText(errorMessage)

    # Appelé quand  on presse le bouton OK
    @Slot()
    def onApplyNewValues(self):
        options = self.m_gamesManager.options
        options.pathToDicos = self.lineEditDicosPath.text()
        options.lettersCount = self.spinBoxLettersCount.value()
        options.duration = self.spinBoxDuration.value()
        options.maximumTriesCount = self.spinBoxMaxTriesCount.value()
        self.m_gamesManager.options = options

    # Appelé quand  on presse le bouton Cancel
    @Slot()
    def onCancel(self):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        self.labelStatus.setText("")
