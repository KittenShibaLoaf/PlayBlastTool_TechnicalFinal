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


class AnimEntry(QWidget):
    entryNameChanged = Signal(str)
    entryRemoved = Signal(AnimClip)
    def __init__(self, animClip: AnimClip):
        super().__init__()
        self.animClip = animClip
        self.masterLayout = QHBoxLayout()
        self.setLayout(self.masterLayout)

        self.toggleBox = QCheckBox()
        self.toggleBox.setChecked(animClip.shouldExport)
        self.toggleBox.toggled.connect(self.ToggleBoxToggled)
        self.masterLayout.addWidget(self.toggleBox)

        subfixLabel = QLabel("Subfix: ")
        self.masterLayout.addWidget(subfixLabel)
        self.subfixLineEdit = QLineEdit()
        self.subfixLineEdit.setValidator(QRegExpValidator('\w+'))
        self.subfixLineEdit.textChanged.connect(self.SubfixTextChanged)
        self.subfixLineEdit.setText(animClip.subfix)
        self.masterLayout.addWidget(self.subfixLineEdit)

        startFrameLabel = QLabel("Start: ")
        self.masterLayout.addWidget(startFrameLabel)
        self.startFrameLineEdit = QLineEdit()
        self.startFrameLineEdit.setValidator(QIntValidator())
        self.startFrameLineEdit.textChanged.connect(self.StartFrameTextChanged)
        self.startFrameLineEdit.setText(str(animClip.frameStart))
        self.masterLayout.addWidget(self.startFrameLineEdit)

        endFrameLabel = QLabel("End: ")
        self.masterLayout.addWidget(endFrameLabel)
        self.endFrameLineEdit = QLineEdit()
        self.endFrameLineEdit.setValidator(QIntValidator())
        self.endFrameLineEdit.textChanged.connect(self.EndFrameTextChanged)
        self.endFrameLineEdit.setText(str(animClip.frameEnd))
        self.masterLayout.addWidget(self.endFrameLineEdit)

        setRangeBtn = QPushButton("[ - ]")
        setRangeBtn.clicked.connect(self.SetRangeBtnClicked)
        self.masterLayout.addWidget(setRangeBtn)
        
        removeBtn = QPushButton("[ X ]")
        removeBtn.clicked.connect(self.RemoveBtnClicked)
        self.masterLayout.addWidget(removeBtn)

    def SubfixTextChanged(self):
        if self.subfixLineEdit.text():
            self.animClip.subfix = self.subfixLineEdit.text()
            self.entryNameChanged.emit(self.animClip.subfix)

    def StartFrameTextChanged(self):
        if self.startFrameLineEdit.text():
            self.animClip.frameEnd = int(self.startFrameLineEdit.text())

    def EndFrameTextChanged(self):
        if self.endFrameLineEdit.text():
            self.animClip.frameStart = int(self.endFrameLineEdit.text())

    def ToggleBoxToggled(self):
        self.animClip.shouldExport = not self.animClip.shouldExport

    def SetRangeBtnClicked(self):
        mc.playbackOptions(minTime = self.animClip.frameStart, maxTime = self.animClip.frameEnd, e = True)

    def RemoveBtnClicked(self):
        self.entryRemoved.emit(self.animClip) # This calls the function connected to the entryRemoved Signal
        self.deleteLater() # Remove this widget the next time it is proper 

class PlayBlastTool:
    def __init__(self):
        self.fileName = ""
        self.animations = []
        self.saveDir = ""

    def GetAnimFolder(self):
        path = os.path.join(self.saveDir, "anim")
        return os.path.normpath(path)

    def GetAnimClipSavePath(self, clip: AnimClip):
        path = os.path.join(self.GetAnimFolder(), self.fileName + "_" + clip.subfix + ".fbx")
        return os.path.normpath(path)
    
    def AddAnimClip(self):
        self.animations.append(AnimClip())
        return self.animations[-1]
    
class PlayBlastWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.playblastTool = PlayBlastTool()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.setFixedWidth(500)
        
        addAnimEntryBtn = QPushButton("Add Your Animation Clip")
        addAnimEntryBtn.clicked.connect(self.AddNewAnimEntryBtnClicked)
        self.masterLayout.addWidget(addAnimEntryBtn)


    def UpdateSavePreview(self):
        previewText = ""
        
        if self.playblastTool.animations:
            for anim in self.playblastTool.animations:
                animPath = self.playblastTool.GetAnimClipSavePath(anim)
                previewText += "\n" + animPath

    def AddNewAnimEntryBtnClicked(self):
        newClip = self.playblastTool.AddAnimClip()
        newEntry = AnimEntry(newClip)
        newEntry.entryRemoved.connect(self.RemoveAnimEntry)
        newEntry.entryNameChanged.connect(self.UpdateSavePreview)
        self.animEntryLayout.addWidget(newEntry)
        self.UpdateSavePreview()

    def RemoveAnimEntry(self, clipToRemove):
        self.adjustSize()
        self.playblastTool.animations.remove(clipToRemove)
        self.UpdateSavePreview()


playblastWidget = AnimEntry()
playblastWidget.show()