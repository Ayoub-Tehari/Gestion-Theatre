
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from action_fct_comp_4_2 import AppFctComp4_2

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4_1(QDialog):

    tache_2_dialog_1 = None
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4_1.ui", self)
        self.data = data
        self.refreshCatList1()

    # Fonction de mise à jour des catégories
    @pyqtSlot()

    def refreshCatList1(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noDos FROM LesDossiers_base")
        except Exception as e:
            self.ui.comboBox_fct_4.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4, result)


    # En cas de clic sur valider
    def envoyer(self):
        if self.fct_comp_4_2_dialog is not None:
            self.fct_comp_4_2_dialog.close()

        self.fct_comp_4_2_dialog = AppFctComp4_2(self.data, self.ui.comboBox_fct_4.currentText())
        self.fct_comp_4_2_dialog.show()
