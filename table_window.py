import json

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.uic.properties import QtGui
from win32api import GetSystemMetrics


class FETable(QTableWidget):

    def __init__(self, number):
        super().__init__()

        # Basic table setup
        self.setWindowTitle('Class Roster')

        # Make table default size (Row = 8, Column = 8)
        # TODO Update creation to rely on no. of elements in JSON
        self.setRowCount(8)
        self.setColumnCount(12)
        self.setAlternatingRowColors(True)
        self.buildWithRoster(number)
        self.addActionColumns()
        headerLabels = ['Name', 'Class', 'Lvl', 'HP', 'Str', 'Mag', 'Dex', 'Spd', 'Lck', 'Def', 'Res', 'Charm', 'Lvl Up', 'Re-Class', 'Kill']
        self.setHorizontalHeaderLabels(headerLabels)
        self.resizeColumnsToContents()
        self.setGeometry(0, 0, 775, 325)

    def buildWithRoster(self, houseNumber):
        if houseNumber == 0:
            targetHouse = 'black_eagle_house_base.json'
        elif houseNumber == 1:
            targetHouse = 'blue_lion_house_base.json'
        else:
            targetHouse = 'yellow_deer_house_base.json'

        rosterCount = 0
        with open('./Notes_and_Such/data_storage/{}'.format(targetHouse)) as jsonFile:
            roster = json.load(jsonFile)
            for count, member in enumerate(roster):
                rosterCount += 1
                Name = member['first_name']
                self.populateTable(count, Name, member['class'],  member['stats'])
        self.addMainCharacter(rosterCount)
        self.addDefaultLevels()

    def populateTable(self, rosterNumber, Name, className,  *args):
        # *args will always contain the amount we expect, 9 stats per member
        self.setItem(rosterNumber, 0, QTableWidgetItem(Name))
        self.setItem(rosterNumber, 1, QTableWidgetItem(className))

        statCount = range(9)
        for place in statCount:
            # Offset by 3 to account for Name, Class and Level columns
            self.setItem(rosterNumber, place + 3, QTableWidgetItem(str(args[0][place])))

    def addMainCharacter(self, rosterNumber):
        # Place MC in lineup
        self.setRowCount(self.rowCount() + 1)
        self.setItem(rosterNumber, 0, QTableWidgetItem("MC (You)"))
        self.setItem(rosterNumber, 1, QTableWidgetItem("Commoner"))
        mainCharacterStats = ["27", "13", "6", "9", "8", "8", "6", "6", "7"]
        for place, entry in enumerate(mainCharacterStats):
            self.setItem(rosterNumber, place + 3, QTableWidgetItem(entry))

    def addDefaultLevels(self):
        for number in range(0, 10):
            self.setItem(number, 2, QTableWidgetItem("1"))

    def addActionColumns(self):
        self.setColumnCount(self.columnCount() + 3)
        for number in range(0, 10):
            levelButton = QPushButton("+1")
            reClassButton = QPushButton("Respec")
            killButton = QPushButton("Ripperoni")
            self.setCellWidget(number, 12, levelButton)
            self.setCellWidget(number, 13, reClassButton)
            self.setCellWidget(number, 14, killButton)


    def show(self):
        super().show()
