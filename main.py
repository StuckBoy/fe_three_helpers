import sys

from table_window import FETable
from PyQt5.QtCore import Qt
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, \
    QLabel, QWidget
from PyQt5.QtGui import QIcon, QPalette, QFont, QColor


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Fire Emblem: Three Houses Helper'
        self.pos()

        # Try to fit in in a good spot, fudge it so the window is as centered as possible
        # TODO rework to specifically reduce dependency on OS (Use link below)
        # https://www.blog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/
        self.left = GetSystemMetrics(0) / 2.75
        self.top = GetSystemMetrics(1) / 2.75

        # This way it fits on the screen
        self.width = GetSystemMetrics(0) / 4
        self.height = GetSystemMetrics(1) / 8
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # Probably could just do all that here
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.buildMenuBar()
        self.buildClassDialog()

        self.setCentralWidget(self.horizontalGroupBox)

        # No going back after showing
        self.show()

    def buildMenuBar(self):
        mainMenuBar = self.menuBar()
        fileMenu = mainMenuBar.addMenu('File')
        self.buildFileMenuStuff(fileMenu)

    def buildFileMenuStuff(self, fileMenu):
        exitButton = QAction(QIcon('./Notes_and_Such/exit24.jpg'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        importButton = QAction(QIcon('./Notes_and_Such/import24.png'), 'Import', self)
        importButton.setShortcut('Ctrl+I')
        importButton.setStatusTip('Import Settings File')
        # TODO Actually do something once the button is TRIGGERED
        # self.openSettingImporter
        fileMenu.addAction(importButton)

        exportButton = QAction(QIcon('./Notes_and_Such/export24.png'), 'Export', self)
        exportButton.setShortcut('Ctrl+E')
        exportButton.setStatusTip('Import Settings File')
        # TODO Actually do something once the button is TRIGGERED
        # self.openSettingExporter
        fileMenu.addAction(exportButton)

    def buildClassDialog(self):
        self.horizontalGroupBox = QGroupBox()
        captionLabel = QLabel("Which class will you be choosing?")
        captionLabel.setFont(QFont('Consolas', 18, QFont.Bold, False))
        captionLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(25, 0, 25, 0)

        buttonBlackEagles = self.generateBasicButton('Black Eagles')
        buttonBlackEagles.clicked.connect(self.selectBlackEagles)
        buttonLayout.addWidget(buttonBlackEagles)

        buttonBlueLions = self.generateBasicButton('Blue Lions')
        buttonBlueLions.clicked.connect(self.selectBlueLions)
        buttonLayout.addWidget(buttonBlueLions)

        buttonYellowDeer = self.generateBasicButton('Yellow Deer')
        buttonYellowDeer.clicked.connect(self.selectYellowDeer)
        buttonLayout.addWidget(buttonYellowDeer)
        buttonLayout.setAlignment(Qt.AlignTop)

        containerLayout = QVBoxLayout()
        containerLayout.addWidget(captionLabel)
        containerLayout.addLayout(buttonLayout)
        self.horizontalGroupBox.setLayout(containerLayout)

    def generateBasicButton(self, caption):
        buttonFont = QFont('Times New Roman', 14, -1, False)
        basicButton = QPushButton(caption, self)
        stylesheetStr = ''
        if caption == 'Black Eagles':
            stylesheetStr = "background-color: salmon"
        elif caption == 'Blue Lions':
            stylesheetStr = "background-color: lightblue"
        elif caption == 'Yellow Deer':
            stylesheetStr = "background-color: yellow"
        basicButton.setStyleSheet(stylesheetStr)
        basicButton.setFont(buttonFont)
        return basicButton

    def selectBlackEagles(self):
        classRoster = FETable(0)
        self.generateClassTable(classRoster)

    def selectBlueLions(self):
        classRoster = FETable(1)
        self.generateClassTable(classRoster)

    def selectYellowDeer(self):
        classRoster = FETable(2)
        self.generateClassTable(classRoster)

    def generateClassTable(self, classRoster):
        tableLayout = QVBoxLayout()
        tableLayout.addWidget(classRoster)
        self.setCentralWidget(classRoster)
        self.resize(classRoster.width(), classRoster.height())


# Rework this in a more OOP Style
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
