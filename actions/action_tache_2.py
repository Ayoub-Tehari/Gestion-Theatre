
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppTache_2 (QDialog):
    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/tache_2.ui", self)
        self.data = data
        self.refreshResult()


    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_tache_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT noSpec, dateRep, promoRep, COALESCE(count(noPlace),0) as nbPlacesReservees FROM LesRepresentations_base left natural join LesTickets group by noSpec, dateRep, promoRep")
        except Exception as e:
            self.ui.tableRepresentations.setRowCount(0)
            display.refreshLabel(self.ui.label_tache_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_tache_2, result)