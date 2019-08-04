import json
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit, QComboBox
from win32api import GetSystemMetrics


def incrementStat(field):
    currentNumber = int(field.text())
    currentNumber += 1
    field.setText(str(currentNumber))


def decrementStat(field):
    currentNumber = int(field.text())
    currentNumber -= 1
    field.setText(str(currentNumber))


class FETable(QTableWidget):

    uniqueClasses = ["Commoner", "Noble", "Dancer"]
    beginnerClasses = ["Myrmidon", "Soldier", "Fighter", "Monk"]
    intermediateClasses = ["Lord", "Mercenary", "Thief", "Cavalier", "Pegasus Knight", "Brigand", "Armored Knight", "Archer", "Brawler", "Mage", "Dark Mage", "Priest"]
    advancedClasses = ["Swordmaster", "Hero", "Assassin", "Paladin", "Warrior", "Fortress Knight", "Wyvern Rider", "Sniper", "Grappler", "Warlock", "Dark Bishop", "Bishop"]
    lordAdvancedClasses = [] # TODO Populate once I'm no longer spoiled
    masterClasses = ["Mortal Savant", "Falcon Knight", "War Master", "Wyvern Lord", "Great Knight", "Bow Knight", "Gremory", "Dark Knight", "Holy Knight"]
    lordMasterClasses = [] # TODO Populate once I'm no longer spoiled
    unknownClasses = [] # TODO Populate once I'm no longer spoiled
    classListCollection = [uniqueClasses, beginnerClasses, intermediateClasses, advancedClasses, lordAdvancedClasses, masterClasses, lordMasterClasses, unknownClasses]

    statList = ['HP', 'Str', 'Mag', 'Dex', 'Spd', 'Lck', 'Def', 'Res', 'Charm']

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
        headerLabels = ['Name', 'Class', 'Lvl']
        headerLabels.extend(self.statList)
        headerLabels.extend(['Lvl Up', 'Re-Class', 'Kill'])
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
        levelButtons = []
        killButtons = []
        for number in range(0, 10):
            levelButtons.append(QPushButton("+1"))
            reClassButton = QPushButton("Respec")
            killButtons.append(QPushButton("Ripperoni"))

            levelButtons[number].clicked.connect(lambda: self.triggerLevelUp())
            reClassButton.clicked.connect(lambda: self.triggerReClass())
            killButtons[number].clicked.connect(lambda: self.triggerKill())

            self.setCellWidget(number, 12, levelButtons[number])
            self.setCellWidget(number, 13, reClassButton)
            self.setCellWidget(number, 14, killButtons[number])

    def triggerLevelUp(self):
        # Generate layout stuff
        levelUpDialog = QDialog()
        levelUpDialog.setWindowTitle("Level Up Student")
        levelUpDialog.setWhatsThis("This modal allows you to level up a particular unit.")
        levelUpDialog.setGeometry(GetSystemMetrics(0) / 2.3, GetSystemMetrics(1) / 2.3, 400, 400)

        dialogText = QLabel("Please increment the stats that the character gained.", levelUpDialog)
        dialogText.move(10, 10)

        buttonConfirm = QPushButton("Confirm", levelUpDialog)
        buttonCancel = QPushButton("Cancel", levelUpDialog)

        buttonConfirm.clicked.connect(levelUpDialog.accept)
        buttonCancel.clicked.connect(levelUpDialog.reject)

        buttonConfirm.move(levelUpDialog.width() - 90, levelUpDialog.height() - 40)
        buttonCancel.move(levelUpDialog.width() - 180, levelUpDialog.height() - 40)

        # Add current stat stuff
        heightOffset = 0
        currentColumn = 3

        statLabels = []
        statFields = []
        incrementButtons = []
        decrementButtons = []

        for x in range(9):
            statLabels.append(QLabel(self.statList[x], levelUpDialog))
            statLabels[x].move(30, 50 + heightOffset)

            statFields.append(QLineEdit(levelUpDialog))
            statFields[x].setReadOnly(True)
            statFields[x].setText(self.item(self.currentRow(), currentColumn).text())
            currentColumn += 1
            statFields[x].setGeometry(70, 45 + heightOffset, 30, 25)

            incrementButtons.append(QPushButton("+", levelUpDialog))
            decrementButtons.append(QPushButton("-", levelUpDialog))

            incrementButtons[x].setGeometry(130, 47 + heightOffset, 20, 20)
            decrementButtons[x].setGeometry(110, 47 + heightOffset, 20, 20)

            heightOffset += 35

            incrementButtons[x].clicked.connect(partial(incrementStat, statFields[x]))
            decrementButtons[x].clicked.connect(partial(decrementStat, statFields[x]))

        levelUpDialog.setWindowModality(Qt.ApplicationModal)
        levelUpDialog.exec_()
        if levelUpDialog.result():
            print("Dialog accepted, updating person in row " + str(self.currentRow()))
            for y in range(9):
                self.item(self.currentRow(), y + 3).setText(statFields[y].text())
            currentLevel = int(self.item(self.currentRow(), 2).text())
            self.item(self.currentRow(), 2).setText(str(currentLevel + 1))
            self.viewport().update()

    def triggerReClass(self):
        # Generate layout stuff
        reClassDialog = QDialog()
        reClassDialog.setWindowTitle("Re-Class Student")
        reClassDialog.setWhatsThis("This modal allows you to change the current class for a particular unit.")
        reClassDialog.setGeometry(GetSystemMetrics(0) / 2.3, GetSystemMetrics(1) / 2.3, 275, 150)

        dialogText = QLabel("Please select the new class from the drop-down.", reClassDialog)
        dialogText.move(10, 10)

        buttonConfirm = QPushButton("Confirm", reClassDialog)
        buttonCancel = QPushButton("Cancel", reClassDialog)

        buttonConfirm.clicked.connect(reClassDialog.accept)
        buttonCancel.clicked.connect(reClassDialog.reject)

        buttonConfirm.move(reClassDialog.width() - 90, reClassDialog.height() - 40)
        buttonCancel.move(reClassDialog.width() - 180, reClassDialog.height() - 40)

        classCombobox = QComboBox(reClassDialog)
        classCombobox.setInsertPolicy(QComboBox.InsertAlphabetically)
        classCombobox.move(90, 50)

        # Get character's current level, and build drop-down based off possible classes
        currentLevel = int(self.item(self.currentRow(), 2).text())
        availableClasses = []
        if currentLevel < 5:
            availableClasses.extend(self.uniqueClasses)
        elif 5 <= currentLevel < 10:
            availableClasses.extend(self.uniqueClasses)
            availableClasses.extend(self.beginnerClasses)
        elif 10 <= currentLevel < 20:
            availableClasses.extend(self.uniqueClasses)
            availableClasses.extend(self.beginnerClasses)
            availableClasses.extend(self.intermediateClasses)
        elif 20 <= currentLevel < 30:
            availableClasses.extend(self.uniqueClasses)
            availableClasses.extend(self.beginnerClasses)
            availableClasses.extend(self.intermediateClasses)
            availableClasses.extend(self.advancedClasses)
        elif currentLevel >= 30:
            availableClasses.extend(self.uniqueClasses)
            availableClasses.extend(self.beginnerClasses)
            availableClasses.extend(self.intermediateClasses)
            availableClasses.extend(self.advancedClasses)
            availableClasses.extend(self.masterClasses)

        availableClasses.sort()
        classCombobox.addItems(availableClasses)
        reClassDialog.setWindowModality(Qt.ApplicationModal)
        reClassDialog.exec_()
        if reClassDialog.result():
            print("Dialog accepted, updating person in row " + str(self.currentRow()))
            self.item(self.currentRow(), 1).setText(classCombobox.currentText())
            self.viewport().update()

    def triggerKill(self):
        killDialog = QDialog()
        killDialog.setWindowTitle("Retire Student Confirmation")
        killDialog.setWhatsThis("This modal allows you to confirm that you lost a student while on a field trip.")
        killDialog.setGeometry(GetSystemMetrics(0) / 2.3, GetSystemMetrics(1) / 2.3, 400, 200)

        dialogText = QLabel("Are you sure you want to permanently retire this person?", killDialog)
        dialogText.move(70, 70)

        buttonConfirm = QPushButton("Confirm", killDialog)
        buttonCancel = QPushButton("Cancel", killDialog)

        buttonConfirm.clicked.connect(killDialog.accept)
        buttonCancel.clicked.connect(killDialog.reject)

        buttonConfirm.move(220, 120)
        buttonCancel.move(130, 120)

        killDialog.setWindowModality(Qt.ApplicationModal)
        killDialog.exec_()
        if killDialog.result():
            print("Dialog accepted, removing person in row " + str(self.currentRow()))
            self.removeRow(int(self.currentRow()))
            self.viewport().update()

    def show(self):
        super().show()
