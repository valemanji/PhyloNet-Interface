import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtLocation
from PyQt5.QtGui import QIcon, QPixmap

import module.launcher
import PostProcessingModule.menu

from styling import *
from functions import *


def resource_path(relative_path):
    """
    Refer to the location of a file at run-time.
    This function is from
    https://www.reddit.com/r/learnpython/comments/4kjie3/how_to_include_gui_images_with_pyinstaller/
    For more information, visit https://pythonhosted.org/PyInstaller/runtime-information.html#run-time-information
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.initUI()

    def initUI(self):
        """
        Initialize GUI.
        """
        self.setWindowTitle("Phylonet") 
        self.setWindowIcon(QIcon("logo.png"))
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint 
                    | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        #flags =  QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(flags)

        wid = QWidget()
        self.setCentralWidget(wid)
        self.setContentsMargins(100, 0, 100, 80)
        ico = QIcon("info.svg")

        infoButton = QPushButton(self)

        #infoButton.setObjectName("infoButton")
        infoButton.clicked.connect(self.aboutMessage)
        infoButton.setIcon(ico)
        infoButton.setFixedSize(48, 48)
        infoButton.setIconSize(infoButton.size())

        infoButton.setStyleSheet("border: none;") 

        # Buttons of two options
        generateBtn = QPushButton(
            "Generate input NEXUS file for PhyloNet", self)
        generateBtn.setObjectName("inputBtn")
        postProcessBtn = QPushButton(
            "Display results of PhyloNet commands", self)
        postProcessBtn.setObjectName("outputBtn")

        generateBtn.clicked.connect(self.openModule)
        postProcessBtn.clicked.connect(self.openPostProcess)


        # Question
        questionLabel = QLabel()
        questionLabel.setObjectName("questionLabel")
        questionLabel.setText(
            "What would you like to do?")

        # Bottom level options
        #this is deceptive, it's no longer horizontal
        hbox = QVBoxLayout()
        hbox.addWidget(generateBtn, alignment=QtCore.Qt.AlignCenter)
        hbox.addWidget(postProcessBtn, alignment=QtCore.Qt.AlignCenter)

        # Main vertical layout.
        vbox = QVBoxLayout()
        #info button gotta go
        #vbox.addWidget(getInfoButton(self))
        vbox.addWidget(infoButton, alignment=QtCore.Qt.AlignRight)
        vbox.addWidget(questionLabel)
        vbox.addLayout(hbox)
        wid.setLayout(vbox)

        #vbox.setContentsMargins(50, 80, 50, 50)

        # menubar.setNativeMenuBar(False)
        #self.setWindowTitle('PhyloNetCompanion')
        #self.setWindowIcon(QIcon(resource_path("logo.png")))

        #size fluidity
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        #sizePolicy.setHorizontalStretch(1)
        #sizePolicy.setVerticalStretch(1)
        #sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        #self.setSizePolicy(sizePolicy)

    
    def link(self, linkStr):
        """
        Open the website of PhyloNet if user clicks on the hyperlink.
        """
        QDesktopServices.openUrl(QtCore.QUrl(linkStr))

    def aboutMessage(self):
        msg = QDialog()
        msg.setWindowTitle("Phylonet") 
        msg.setWindowIcon(QIcon("logo.png"))
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint )
        msg.setWindowFlags(flags)
        msg.setObjectName("aboutMessage")

        vbox = QVBoxLayout()
        text = QLabel("PhyloNet is a tool designed mainly for analyzing, "
                    "reconstructing, and evaluating reticulate "
                    "(or non-treelike) evolutionary relationships, "
                    "generally known as phylogenetic networks. Various "
                    "methods that we have developed make use of techniques "
                    "and tools from the domain of phylogenetic trees, and "
                    "hence the PhyloNet package includes several tools for "
                    "phylogenetic tree analysis. PhyloNet is released under "
                    "the GNU General Public License. \n\nPhyloNet is designed, "
                    "implemented, and maintained by Rice's BioInformatics Group, "
                    "which is lead by Professor Luay Nakhleh (nakhleh@cs.rice.edu). ")

        text.setWordWrap(True)
        text.setStyleSheet("padding: 60px 100px 10px 100px;")
        
        hyperlink = QLabel()
        hyperlink.setText('For more details related to this group please visit '
                          '<a href="http://bioinfo.cs.rice.edu">'
                          'http://bioinfo.cs.rice.edu</a>.')
        hyperlink.linkActivated.connect(self.link)
        hyperlink.setStyleSheet("padding: 10px 100px 80px 100px;")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.clicked.connect(msg.accept)
        vbox.addWidget(text)
        vbox.addWidget(hyperlink)
        vbox.addWidget(buttonBox)
        msg.setLayout(vbox)
        msg.exec_()

    def openModule(self):
        self.nexGenerator = module.launcher.Launcher()
        self.nexGenerator.show()
        #Closes main window so its cleaner for user
        #self.window().setVisible(False)

    def openPostProcess(self):
        self.outputSummarizer = PostProcessingModule.menu.MenuPage()
        self.outputSummarizer.show()
        #same as above
        #self.window().setVisible(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style())
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
