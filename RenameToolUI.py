try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
from maya import cmds
import importlib, os
from . import RenameToolUtil as Reui
importlib.reload(Reui)


class AnimatedButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: transparent;
                border: 2px solid #FF723D;
                text-transform: uppercase;
                font-family: "Aldrich";
                letter-spacing: 2px;
                font-size: 16px;
                font-weight: bold;
            }
        ''')

    
        self.overlay = QtWidgets.QFrame(self)
        self.overlay.setStyleSheet("background-color: #FF723D;")
        self.overlay.setGeometry(-100, 0, 0, self.height())
        self.overlay.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect(self.overlay))
        self.overlay.graphicsEffect().setOpacity(0.5)

        
        self.anim = QtCore.QPropertyAnimation(self.overlay, b"geometry")
        self.anim.setDuration(800)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def enterEvent(self, event):
        
        self.anim.stop()
        start_rect = QtCore.QRect(-100, 0, 0, self.height())
        end_rect = QtCore.QRect(-20, 0, self.width() + 100, self.height())
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()

        
        self.setStyleSheet('''
            QPushButton {
                color: #833ab4;
                background-color: transparent;
                border: 2px solid #FF723D;
                text-transform: uppercase;
                font-family: "Aldrich";
                letter-spacing: 2px;
                font-size: 16px;
                font-weight: bold;
            }
        ''')

    def leaveEvent(self, event):
       
        self.anim.stop()
        start_rect = self.overlay.geometry()
        end_rect = QtCore.QRect(-100, 0, 0, self.height())
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()

        
        self.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: transparent;
                border: 2px solid #FF723D;
                text-transform: uppercase;
                font-family: "Aldrich";
                letter-spacing: 2px;
                font-size: 16px;
                font-weight: bold;
            }
        ''')

#__________________________________________________________________________________#

class MyStyleToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyStyleToolDialog, self).__init__(parent)
        self.setWindowTitle('RENAME TOOL')
        self.resize(700, 450)
        self.setStyleSheet('background-color: #333333;') 

       
        self.script_dir = os.path.dirname(__file__)

        # ---------- MAIN LAYOUT ----------
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.mainLayout.setContentsMargins(15, 15, 15, 15)
        self.mainLayout.setSpacing(10)
        self.setLayout(self.mainLayout)

        # ---------- TITLE ----------
        self.titleLabel = QtWidgets.QLabel("RENAME TOOL")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet('''
            QLabel {
                color: #E0E0E0;
                font-size: 18px;
                font-family: "Aldrich";
                font-weight: bold;
            }
        ''')
        self.mainLayout.addWidget(self.titleLabel, 0, 1, 1, 2) 

        # ---------- SPINE ANIMATION (GIF) ----------
        self.animLabel = QtWidgets.QLabel()
        self.mainLayout.addWidget(self.animLabel, 1, 0, 4, 1, alignment=QtCore.Qt.AlignCenter)

        
        gif_path = os.path.join(self.script_dir, "resourches", "image", "Benedict Cumberbatch Magic GIF by Spider-Man (1).gif")
        gif_path = gif_path.replace("\\", "/") 

        self.movie = QtGui.QMovie(gif_path)
        if not self.movie.isValid():
            print(f"❌ ไม่พบไฟล์ GIF ที่ระบุ: {gif_path}")
        else:
            self.animLabel.setMovie(self.movie)
            self.movie.setScaledSize(QtCore.QSize(200, 200)) 
            self.movie.start()

        # ---------- COMBO ----------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Search and replace name", "Rename", "Prefix", "Suffix"])
        self.comboBox.setStyleSheet('''
            QComboBox {
                background-color: #A1024E;
                color: #2F2F2F;
                border-radius: 3px;
                font-size: 16px;
                padding: 4px;
                font-family: "Aldrich";
                font-weight: bold;
            }
            QComboBox:hover { background-color: #FF5C8F; }
            QComboBox::drop-down { border: 0px; }
        ''')
        self.mainLayout.addWidget(self.comboBox, 1, 1, 1, 2)

        # ---------- RadioButton ----------
        self.radioLayout = QtWidgets.QHBoxLayout()
        self.radioLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.hierarchyCheck = QtWidgets.QRadioButton("Hierarchy")
        self.selectedCheck = QtWidgets.QRadioButton("Selected")
        self.allCheck = QtWidgets.QRadioButton("All")
        self.selectedCheck.setChecked(True) 

        for cb in [self.hierarchyCheck, self.selectedCheck, self.allCheck]:
            cb.setStyleSheet('''
                QRadioButton {
                    font-size: 16px;
                    color: #CCCCCC;
                    font-family: "Aldrich";
                    padding: 4px;
                    spacing: 20px;
                }
                QRadioButton::indicator {
                    width: 16px; height: 16px;
                }
                QRadioButton::indicator:checked {
                    background-color: #FF5C8F;
                    border: 2px solid #2F2F2F;
                    border-radius: 9px;
                }
                QRadioButton::indicator:unchecked {
                    background-color: #444;
                    border: 2px solid #aaa;
                    border-radius: 9px;
                }
            ''')
            self.radioLayout.addWidget(cb)
        self.mainLayout.addLayout(self.radioLayout, 2, 1, 1, 2)

        # ---------- INPUT ----------
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.newNameLineEdit = QtWidgets.QLineEdit()
        for le in [self.nameLineEdit, self.newNameLineEdit]:
            le.setStyleSheet('''
                QLineEdit {
                    color: white;
                    background-color: #474747;
                    font-family: "Aldrich";
                    font-size: 16px;
                    font-weight: bold;
                    padding: 5px;
                    border-radius: 3px;
                }
            ''')
        self.mainLayout.addWidget(self.nameLineEdit, 3, 1, 1, 2)
        self.mainLayout.addWidget(self.newNameLineEdit, 4, 1, 1, 2)

        # ---------- BUTTON ----------
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.applyButton = AnimatedButton('Apply')
        self.cancelButton = AnimatedButton('Cancel')
        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(self.buttonLayout, 5, 1, 1, 2)

        # ---------- CONNECTIONS ----------
        self.applyButton.clicked.connect(self.onApplyClicked)
        self.cancelButton.clicked.connect(self.close)
        
        self.comboBox.currentTextChanged.connect(self.update_ui_mode)

        
        self.update_ui_mode(self.comboBox.currentText())

    def update_ui_mode(self, mode_text):
        if mode_text == "Search and replace name":
            self.nameLineEdit.show()
            self.nameLineEdit.setPlaceholderText("SEARCH NAME")
            self.newNameLineEdit.setPlaceholderText("REPLACE WITH")
        else:
            self.nameLineEdit.hide()
            if mode_text == "Rename":
                self.newNameLineEdit.setPlaceholderText("ENTER NEW NAME")
            elif mode_text == "Prefix":
                self.newNameLineEdit.setPlaceholderText("ENTER PREFIX")
            elif mode_text == "Suffix":
                self.newNameLineEdit.setPlaceholderText("ENTER SUFFIX")

    def showSuccessGif(self):
    
        GIF_PATH = os.path.join(self.script_dir, "resourches", "image", "Benedict Cumberbatch Magic GIF by Spider-Man.gif")
        GIF_PATH = GIF_PATH.replace("\\", "/")

        if not os.path.exists(GIF_PATH):
            QtWidgets.QMessageBox.warning(self, "GIF not found", f"ไม่พบไฟล์:\n{GIF_PATH}")
            return

        self.gifDialog = QtWidgets.QDialog(self)
        self.gifDialog.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        self.gifDialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.gifDialog.setFixedSize(500, 500)

        layout = QtWidgets.QVBoxLayout(self.gifDialog)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(self.gifDialog)
        layout.addWidget(label)

        movie = QtGui.QMovie(GIF_PATH)
        movie.setScaledSize(QtCore.QSize(700, 700))
        label.setMovie(movie)
        movie.start()

        QtCore.QTimer.singleShot(2800, self.gifDialog.accept) 
        self.gifDialog.exec_()

    def onApplyClicked(self):
        old_name = self.nameLineEdit.text().strip()
        new_name = self.newNameLineEdit.text().strip()
        mode = self.comboBox.currentText()

        scope = "All" 
        if self.hierarchyCheck.isChecked():
            scope = "Hierarchy"
        elif self.selectedCheck.isChecked():
            scope = "Selected"

        try:
            Reui.process(mode, old_name, new_name, scope)
           
            self.showSuccessGif()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"❌ Failed to process:\n{e}")


def run():
    global ui
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MyStyleToolDialog(parent=ptr)
    ui.show()