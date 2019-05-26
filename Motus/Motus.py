import sys
from PySide2.QtWidgets import QApplication

import ui.MainWindow  as MainWindow
import game_engine.GamesManager as GamesManager

if __name__ == "__main__":
    # Création de l'application Qt
    app = QApplication(sys.argv)

    # Création de la fenêtre principale
    mainWindow = MainWindow.MainWindow(GamesManager.GamesManager())

    # Affichage de la fenêtre à l'écran
    mainWindow.show()

    # Exécution de l'application
    sys.exit(app.exec_())