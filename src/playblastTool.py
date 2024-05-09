import os
import maya.cmds as mc
from PySide2.QtCore import Signal
from PySide2.QtGui import QIntValidator, QRegExpValidator
from PySide2.QtWidgets import QWidget, QAbstractItemView, QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget


class AnimClip:
    def __init__(self):
        self.frameStart = int(mc.playbackOptions(q = True, min = True))
        self.frameEnd = int(mc.playbackOptions(q = True, max = True))
        self.subfix = ""
        self.shouldExport = True

class MayaPlayblastTool:
    def __init__(self):
        self.saveDir = ""

    def SetSaveDir(self, newSaveDir):
        self.saveDir = newSaveDir

class MayaPlayblastWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.mayaPlayblast = MayaPlayblastTool()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.setFixedWidth(250)

    def UpdateSavePreview(self):
        pass

mayaPlayblastWidget = MayaPlayblastWidget()
mayaPlayblastWidget.show()