import os
import maya.cmds as mc
from PySide2.QtCore import Signal
from PySide2.QtGui import QIntValidator, QRegExpValidator
from PySide2.QtWidgets import QWidget, QAbstractItemView, QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget

class MayaPlayblastTool:
    def __init__(self):
        self.saveDir = ""
        self.saveName = ""

    def SetSaveDir(self, newSaveDir):
        self.saveDir = newSaveDir

    def SetSaveName(self, newName):
        self.saveName = newName

    def GetSavePath(self):
        path = os.path.join(self.saveDir, self.saveName + ".mov")
        return os.path.normpath(path)

class MayaPlayblastWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mayaPlayblast = MayaPlayblastTool()
        self.masterLayout = QVBoxLayout()
        self.setWindowTitle("Playblast Tool!")
        self.setLayout(self.masterLayout)
        self.setFixedWidth(500)

        playblastBtn = QPushButton("Playblast Current Window")
        playblastBtn.clicked.connect(self.PlayblastBtnClicked)
        self.masterLayout.addWidget(playblastBtn)

        self.saveFileLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.saveFileLayout)
        fileNameLabel = QLabel("Name: ")
        self.saveFileLayout.addWidget(fileNameLabel)
        self.fileNameLineEdit = QLineEdit()
        self.fileNameLineEdit.setFixedWidth(50)
        self.fileNameLineEdit.setValidator(QRegExpValidator("\w+"))
        self.fileNameLineEdit.textChanged.connect(self.FileNameChanged)
        self.saveFileLayout.addWidget(self.fileNameLineEdit)

        fileDirLabel = QLabel("Save Directory: ")
        self.saveFileLayout.addWidget(fileDirLabel)
        self.saveDirLineEdit = QLineEdit()
        self.saveDirLineEdit.setEnabled(False)
        self.saveFileLayout.addWidget(self.saveDirLineEdit)

        setSaveDirBtn = QPushButton("...")
        setSaveDirBtn.clicked.connect(self.SetSaveDirBtnClicked)
        self.saveFileLayout.addWidget(setSaveDirBtn)

        self.savePreviewLabel = QLabel()
        self.masterLayout.addWidget(self.savePreviewLabel)

    def UpdateSavePreview(self):
        previewText = ""
        self.savePreviewLabel.setText(previewText)
        self.adjustSize()

    def PlayblastBtnClicked(self):
        print(f"saving to: {self.mayaPlayblast.GetSavePath()}")
        mc.playblast(format = "qt", filename = self.mayaPlayblast.GetSavePath(), sequenceTime = 0, clearCache = 1, viewer = 1, showOrnaments = 1, fp = 4, percent = 100, compression = "H.264", quality = 100, widthHeight = (1920, 1080), forceOverwrite = 1)

    def FileNameChanged(self, newName):
        self.mayaPlayblast.SetSaveName(newName)
        self.UpdateSavePreview()

    def SetSaveDirBtnClicked(self):
        # path = mc.fileDialog2(dir = "~/", dialogStyle = 2, fileMode = 3)
        # This selects folders through Maya 
            # path = mc.fileDialog2(dir = "~/", dialogStyle = 2, fileMode = 3)

        # This selects folders through Windows. This is a better option as it doesn't rely on Maya
        dir = QFileDialog().getExistingDirectory()
        self.mayaPlayblast.SetSaveDir(dir)
        self.saveDirLineEdit.setText(dir)
        self.UpdateSavePreview()


mayaPlayblastWidget = MayaPlayblastWidget()
mayaPlayblastWidget.show()