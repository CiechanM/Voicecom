from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtTest

import client
import sys, time
import re, os

ip_regex = "^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"

class Okno(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Okno, self).__init__(*args, *kwargs)
        self.setWindowTitle("VOICECOM")

        # Client part
        self.voice_client = client.Client()

        # joining server window
        titleText = QLabel()
        titleText.setText("VOICECOM")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Courier New', 35))
        titleText.setStyleSheet("QLabel {color: #1B2A41} ")

        connectText = QLabel()
        connectText.setText("CONNECT TO SERVER")
        connectText.setAlignment(Qt.AlignCenter)
        connectText.setFont(QFont('Courier New', 20))
        connectText.setStyleSheet("QLabel {color: #1B2A41} ")

        self.nickField = QLineEdit()
        self.nickField.setPlaceholderText("*Nickname*")
        self.nickField.setFont(QFont('Courier New', 11))
        self.nickField.setStyleSheet("QLineEdit {color: #000000}")

        self.ipField = QLineEdit()
        self.ipField.setPlaceholderText("*IP Address*")
        self.ipField.setFont(QFont('Courier New', 11))
        self.ipField.setStyleSheet("QLineEdit {color: #000000}")

        self.portField = QLineEdit()
        self.portField.setPlaceholderText("*Port*")
        self.portField.setFont(QFont('Courier New', 11))
        self.portField.setStyleSheet("QLineEdit {color: #1B2A41}")

        connectButton = QPushButton()
        connectButton.setText("CONNECT")
        connectButton.setFont(QFont('Courier New', 12))
        connectButton.setStyleSheet("QPushButton {background : #1B2A41}")
        connectButton.setStyleSheet("QPushButton {color : #1B2A41}")
        connectButton.clicked.connect(self.connectClicked)

        connectButtonsLayout = QHBoxLayout()
        connectButtonsLayout.addWidget(connectButton)
        connectButtonsLayoutW = QWidget()
        connectButtonsLayoutW.setLayout(connectButtonsLayout)

        self.connectWindow = QVBoxLayout()
        self.connectWindow.addWidget(titleText)
        self.connectWindow.addWidget(connectText)
        self.connectWindow.addWidget(self.nickField)
        self.connectWindow.addWidget(self.ipField)
        self.connectWindow.addWidget(self.portField)
        self.connectWindow.addWidget(connectButtonsLayoutW)

        self.connectWindowW = QWidget()
        self.connectWindowW.setLayout(self.connectWindow)

        # server window

        connectedText = QLabel()
        connectedText.setText("CONNECTED TO SERVER")
        connectedText.setAlignment(Qt.AlignCenter)
        connectedText.setFont(QFont('Courier New', 12))
        connectedText.setStyleSheet("QLabel {color: #1B2A41} ")

        self.ipText = QLabel()
        self.ipText.setText("IP ADDRESS")
        self.ipText.setAlignment(Qt.AlignCenter)
        self.ipText.setFont(QFont('Courier New', 12))
        self.ipText.setStyleSheet("QLabel {color: #1B2A41} ")

        self.portText = QLabel()
        self.portText.setText("PORT")
        self.portText.setAlignment(Qt.AlignCenter)
        self.portText.setFont(QFont('Courier New', 12))
        self.portText.setStyleSheet("QLabel {color: #1B2A41} ")

        self.roomChoose = QComboBox(self)
        rooms = ["ROOM 0", "ROOM 1"]
        self.roomChoose.setEditable(True)
        self.roomChoose.addItems(rooms)
        self.roomChoose.activated.connect(self.chooseRoom)
        edit = self.roomChoose.lineEdit()
        edit.setAlignment(Qt.AlignRight)

        self.joinButton = QPushButton()
        self.joinButton.setText("JOIN")
        self.joinButton.setFont(QFont('Courier New', 12))
        self.joinButton.setStyleSheet("QPushButton {background : #1B2A41}")
        self.joinButton.setStyleSheet("QPushButton {color : #1B2A41}")
        self.joinButton.clicked.connect(self.joinClicked)

        self.disconnectButton = QPushButton()
        self.disconnectButton.setText("DISCONNECT")
        self.disconnectButton.setFont(QFont('Courier New', 12))
        self.disconnectButton.setStyleSheet("QPushButton {background : #1B2A41}")
        self.disconnectButton.setStyleSheet("QPushButton {color : #1B2A41}")
        self.disconnectButton.clicked.connect(self.disconnectClicked)

        self.muteButton = QPushButton()
        self.muteButton.setText("MUTE")
        self.muteButton.setFont(QFont('Courier New', 12))
        self.muteButton.setStyleSheet("QPushButton {background : #1B2A41}")
        self.muteButton.setStyleSheet("QPushButton {color : #1B2A41}")
        self.muteButton.clicked.connect(self.muteClicked)

        joinButtonsLayout = QHBoxLayout()
        joinButtonsLayout.addWidget(self.roomChoose)
        joinButtonsLayout.addWidget(self.joinButton)
        joinButtonsLayoutW = QWidget()
        joinButtonsLayoutW.setLayout(joinButtonsLayout)

        self.users = QTextEdit("")
        self.users.setReadOnly(True)
        self.users.setFont(QFont('Courier New', 12))
        self.users.setStyleSheet("QLabel {color: #1B2A41} ")
        #self.users.setAlignment(Qt.AlignCenter)

        usersLayout = QHBoxLayout()
        usersLayout.addWidget(self.users)
        usersW = QWidget()
        usersW.setLayout(usersLayout)

        self.passwordBox = QLineEdit(self)

        self.serverWindow = QVBoxLayout()
        self.serverWindow.addWidget(connectedText)
        self.serverWindow.addWidget(self.ipText)
        self.serverWindow.addWidget(self.portText)
        #self.serverWindow.addWidget(self.users)
        self.serverWindow.addWidget(usersW)
        self.serverWindow.addWidget(joinButtonsLayoutW)
        self.serverWindow.addWidget(self.disconnectButton)
        self.serverWindow.addWidget(self.muteButton)

        self.serverWindowW = QWidget()
        self.serverWindowW.setLayout(self.serverWindow)

        # stack wszystkich ekranow
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.connectWindowW)
        self.Stack.addWidget(self.serverWindowW)

        self.setCentralWidget(self.Stack)

    # connection funcitons
    def connectClicked(self):
        ipAddress = self.ipField.text()
        port = int(self.portField.text())

        if re.search(ip_regex, ipAddress) and port != '' and 1000 < int(port) < 9999:
            try:
                self.voice_client.connect(ipAddress, port)
                self.ipText.setText("IP ADDRESS: " + str(ipAddress))
                self.portText.setText("PORT: " + str(port))
                self.Stack.setCurrentIndex(1)

            except:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Wrong IP address or port.")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Wrong IP address or port.")
            msg.exec_()

    # server functions

    def joinClicked(self):
        correctPassword = "maslo"
        roomNumber = str(self.roomChoose.currentText())[-1]
        nickname = str(self.nickField.text())
        password, ok = QInputDialog.getText(self, '*Password*', 'Enter password')

        while 1:
            if str(password) == str(correctPassword):
                QMessageBox.about(self, "WELCOME", "Correct password")
                try:
                    self.voice_client.room_pick(int(roomNumber), nickname)
                except:
                    print("joining error")
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("joined not")
                    msg.exec_()
                break
            else:
                password, ok = QInputDialog.getText(self, '*Enter correct password*', 'Wrong password')

    def disconnectClicked(self):
        try:
            self.voice_client.disconnect()
            self.Stack.setCurrentIndex(0)
        except:
            print("error")

    def chooseRoom(self):
        pass

    def muteClicked(self):
        print("Mute button clicked")
        muted = self.voice_client.mute()
        if muted == True:
            self.muteButton.setText("UNMUTE")
        else:
            self.muteButton.setText("MUTE")

app = QApplication(sys.argv)

window = Okno()
window.setFixedSize(450, 500)
window.setStyleSheet("background-color:  #CCC9DC ;")
window.show()

app.exec_()