
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from action_fct_comp_4_2 import AppFctComp4_2

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4_2(QDialog):

    tache_2_dialog_1 = None
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4_2.ui", self)
        self.data = data
        self.refreshCatList2()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        # TODO 1.7 : fonction à modifier pour que le numéro de dossier ne puisse être choisi que parmi ceux présents dans la base et que la catégorie ne propose que des valeurs possibles pour le dossier choisi, une fois le fichier ui correspondant mis à jour
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        try:

            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT * FROM LesTickets NATURAL JOIN LesPlaces NATURAL JOIN LesZones WHERE noDos = ? AND catZone=?",
                [self.ui.comboBox_fct_4.currentText(),self.ui.comboBox_4_categorie.currentText()]
            )
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

    # Fonction de mise à jour des catégories
    @pyqtSlot()



    def refreshCatList2(self):

        try:
            self.ui.comboBox_4_categorie.clear()
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT catZone FROM LesZones NATURAL JOIN LesTickets where noDos = ?", [self.ui.comboBox_fct_4.currentText()])
        except Exception as e:
            self.ui.comboBox_4_categorie.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_4_categorie, result)