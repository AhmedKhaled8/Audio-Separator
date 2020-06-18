from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
from os import path
import pathlib



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.save = None
        self.mode = 0
        self.setWindowTitle("Separator")
        self.setWindowIcon(QIcon("images/icons/cut.png"))
        self.mainLayout = QVBoxLayout()
        self.mainGroup = QGroupBox()
        self.setModeSelectionLayout()
        self.buttonsLayout = QHBoxLayout()
        self.buttonsGroup = QGroupBox()
        self.setOpenSongLayout()
        self.setSelectSaveDirectoryLayout()
        self.setConvertLayout()

        self.buttonsGroup.setLayout(self.buttonsLayout)
        self.mainLayout.addWidget(self.buttonsGroup)
        self.mainGroup.setLayout(self.mainLayout)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(200)
        self.setCentralWidget(self.mainGroup)

    def setModeSelectionLayout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        self.vocalsSongMode = QRadioButton("Separate Vocals and Music")
        self.vocalsSongMode.setChecked(True)
        self.vocalsSongMode.setStyleSheet("margin: 10px 20px 10px 20px; font: 14px;")
        self.vocalsSongMode.toggled.connect(self.selectSeparationMode)
        self.instrumentsMode = QRadioButton("Separate Instruments")
        self.instrumentsMode.setChecked(False)
        self.instrumentsMode.setStyleSheet("margin: 10px 20px 10px 20px; font: 14px;")
        self.instrumentsMode.toggled.connect(self.selectSeparationMode)
        layout.addWidget(self.vocalsSongMode)
        layout.addWidget(self.instrumentsMode)
        grb = QGroupBox()
        grb.setLayout(layout)
        self.mainLayout.addWidget(grb)

    def selectSeparationMode(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            if radioBtn.text() == "Separate Vocals and Song":
                self.mode = 0
            elif radioBtn.text() == "Separate Instruments":
                self.mode = 1

    def setOpenSongLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        grb = QGroupBox()
        self.selectSongButton = QPushButton("Select A Song")
        self.selectSongButton.setStyleSheet("font: 16px; padding: 10px; margin-bottom: 5px;")
        self.selectSongButton.setMaximumWidth(300)
        self.selectSongButton.clicked.connect(self.openSong)
        self.songLabel = QLabel("Your song's name")
        self.songLabel.setAlignment(Qt.AlignCenter)
        self.songLabel.setStyleSheet("font: 20px;")
        layout.addWidget(self.selectSongButton)
        layout.addWidget(self.songLabel)
        grb.setLayout(layout)
        self.buttonsLayout.addWidget(grb)

    def setSelectSaveDirectoryLayout(self):
        layout = QVBoxLayout()
        grb = QGroupBox()
        layout.setAlignment(Qt.AlignHCenter)
        self.selectSaveDirectoryButton = QPushButton("Select Save Directory")
        self.selectSaveDirectoryButton.setStyleSheet("font: 16px; padding: 10px; margin-bottom: 5px;")
        self.saveDirectoryLabel = QLabel("Save Directory")
        self.saveDirectoryLabel.setStyleSheet("font: 14px;")
        self.saveDirectoryLabel.setAlignment(Qt.AlignCenter)
        self.selectSaveDirectoryButton.clicked.connect(self.saveFolder)
        layout.addWidget(self.selectSaveDirectoryButton)
        layout.addWidget(self.saveDirectoryLabel)
        grb.setLayout(layout)
        self.buttonsLayout.addWidget(grb)
    
    def setConvertLayout(self):
        layout = QVBoxLayout()
        grb = QGroupBox()
        layout.setAlignment(Qt.AlignHCenter)
        self.convertButton = QPushButton("Separate")
        self.convertButton.setStyleSheet("font: 18px; padding: 10px;")
        self.convertButton.clicked.connect(self.separate)
        layout.addWidget(self.convertButton)
        grb.setLayout(layout)
        self.buttonsLayout.addWidget(grb)
        
    

    def openSong(self):
        options = QFileDialog.Options()
        self.path, _ = QFileDialog.getOpenFileName(self, "Open Song", "", "Song Files (*.mp3)", options=options)
        if self.path:
            print(self.path)
            self.songLabel.setText(self.getFileName(self.path))

    def saveFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.save = QFileDialog.getExistingDirectory(self, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.saveDirectoryLabel.setText(self.save)
        if self.save:
            print(self.save)

    def separate(self):
        if self.path and self.save:
            songPath = "\""+self.path+"\""
            savePath = "\""+self.save+"\""
            # Using embedded configuration.
            # separator = Separator('spleeter:2stems')
            # separator.separate_to_file(self.path, self.save)
            if self.mode == 0:
                cmd = "python -m spleeter separate -i {} -p spleeter:2stems -o {}".format(songPath, savePath)
            elif self.mode == 1:
                cmd = "python -m spleeter separate -i {} -p spleeter:5stems -o {}".format(songPath, savePath)
            os.system(cmd)
            if self.mode == 0:
                fileName = self.getFileName(self.path)
                vocalsFile = pathlib.Path(self.save+"/"+fileName+"/vocals.wav")
                accompanimentFile = pathlib.Path(self.save+"/"+fileName+"/accompaniment.wav")
                if vocalsFile.exists() and accompanimentFile.exists():
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowIcon(QIcon("images/icons/tick.png"))
                    msg.setWindowTitle("Separation Succceded")
                    msg.setText("Separated files are saved into the folder you chose...")
                    msg.exec_()
            elif self.mode == 1:
                fileName = self.getFileName(self.path)
                vocalsFile = pathlib.Path(self.save+"/"+fileName+"/vocals.wav")
                bassFile = pathlib.Path(self.save+"/"+fileName+"/bass.wav")
                pianoFile = pathlib.Path(self.save+"/"+fileName+"/piano.wav")
                drumsFile = pathlib.Path(self.save+"/"+fileName+"/drums.wav")
                otherFile = pathlib.Path(self.save+"/"+fileName+"/other.wav")
                if vocalsFile.exists() and bassFile.exists() and pianoFile.exists() and drumsFile.exists() and otherFile.exists():
                    msg = QMessageBox()
                    msg.setWindowIcon(QIcon("images/icons/tick.png"))
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Separation Succceded")
                    msg.setText("Separated files are saved into the folder you chose...")
                    msg.exec_()



        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(QIcon("images/icons/close.png"))
            if not self.path:
                msg.setWindowTitle("Song not selected")
                msg.setText("Please select a song to separate...")
            elif not self.save:
                msg.setWindowTitle("Folder not selected")
                msg.setText("Please select a folder to save the separated files...")    
            msg.exec_()

    def getFileName(self, path):
        return path.split('.')[-2].split('/')[-1]

app = QApplication(sys.argv)
ui = MainWindow()
ui.show()
sys.exit(app.exec_())

