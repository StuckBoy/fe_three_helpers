import json

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from win32api import GetSystemMetrics


class FETable(QTableWidget):

    def __init__(self, number):
        super().__init__()

        # Basic table setup
        self.setWindowTitle('Class Roster')

        # Make table default size (Row = 8, Column = 8)
        # TODO Update creation to rely on no. of elements in JSON
        self.setRowCount(8)
        self.setColumnCount(11)
        self.setHorizontalHeaderLabels(['Name', 'Class', 'HP', 'Str', 'Mag', 'Dex', 'Spd', 'Lck', 'Def', 'Res', 'Char'])
        self.setGeometry(GetSystemMetrics(0) / 8, GetSystemMetrics(1) / 8, 975, 425)
        self.buildWithRoster(number)
        self.resizeColumnsToContents()

    def buildWithRoster(self, houseNumber):
        if (houseNumber == 0):
            targetHouse = 'black_eagle_house_base.json'
        elif (houseNumber == 1):
            targetHouse = 'blue_lion_house_base.json'
        else:
            targetHouse = 'yellow_deer_house_base.json'
        with open('./Notes_and_Such/data_storage/{}'.format(targetHouse)) as jsonFile:
            roster = json.load(jsonFile)
            for count, member in enumerate(roster):
                Name = member['first_name']
                self.populateTable(count, Name, member['class'],  member['stats'])

    def populateTable(self, rosterNumber, Name, className,  *args):
        # *args will always contain the amount we expect, 9 stats per member
        self.setItem(rosterNumber, 0, QTableWidgetItem(Name))
        self.setItem(rosterNumber, 1, QTableWidgetItem(className))

        statCount = range(9)
        for place in statCount:
            # Offset by 2 to account for Name and Class columns
            self.setItem(rosterNumber, place+2, QTableWidgetItem(str(args[0][place])))

    def show(self):
        super().show()
