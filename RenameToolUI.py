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


class MyStyleToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyStyleToolDialog, self).__init__(parent)
        self.setWindowTitle('RENAME TOOL')
        self.resize(340, 340)
        self.setStyleSheet('background-color: #866d68;')

        # ---------- MAIN LAYOUT ----------
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # ---------- TITLE ----------
        self.titleLabel = QtWidgets.QLabel("RENAME TOOL")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet('''
            QLabel {
                color: white;
                font-size: 18px;
                font-family: "Segoe UI";
                font-weight: bold;
            }
        ''')
        self.mainLayout.addWidget(self.titleLabel)

        # ---------- COMBO ----------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Search and replace name", "Rename", "Prefix hierarchy"])
        self.comboBox.setStyleSheet('''
            QComboBox {
                background-color: #c8a78e;
                color: white;
                border-radius: 6px;
                font-size: 16px;
                padding: 4px;
                font-family: "Segoe UI";
                font-weight: bold;
            }
            QComboBox:hover {
                background-color: #532316;
            }
        ''')
        self.mainLayout.addWidget(self.comboBox)

        # ---------- CHECKBOX ----------
        self.checkboxLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.checkboxLayout)

        self.hierarchyCheck = QtWidgets.QCheckBox("Hierarchy")
        self.selectedCheck = QtWidgets.QCheckBox("Selected")
        self.allCheck = QtWidgets.QCheckBox("All")
        self.selectedCheck.setChecked(True)

        self.checkGroup = QtWidgets.QButtonGroup(self)
        self.checkGroup.setExclusive(True)
        for cb in [self.hierarchyCheck, self.selectedCheck, self.allCheck]:
            self.checkGroup.addButton(cb)
            cb.setStyleSheet('''
                QCheckBox {
                    font-size: 14px;
                    color: white;
                    spacing: 10px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 8px;
                    border: 2px solid white;
                    background-color: transparent;
                }
                QCheckBox::indicator:checked {
                    background-color: #532316;
                    border: 2px solid #532316;
                }
            ''')
            self.checkboxLayout.addWidget(cb)

        # ---------- INPUT ----------
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setPlaceholderText("SEARCH NAME")
        self.newNameLineEdit = QtWidgets.QLineEdit()
        self.newNameLineEdit.setPlaceholderText("NEW NAME")
        for le in [self.nameLineEdit, self.newNameLineEdit]:
            le.setStyleSheet('''
                QLineEdit {
                    color: black;
                    background-color: white;
                    font-size: 18px;
                    font-weight: bold;
                }
            ''')
            self.mainLayout.addWidget(le)

        # ---------- BUTTON ----------
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.applyButton = QtWidgets.QPushButton('Apply')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.applyButton.setStyleSheet('''
            QPushButton {
                background-color: #af2529;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #57141e; }
        ''')
        self.cancelButton.setStyleSheet('''
            QPushButton {
                background-color: #7a2b0f;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #866c75; }
        ''')

        # ---------- SUCCESS GIF ----------
        self.successGifLabel = QtWidgets.QLabel()
        self.successGifLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.successGifLabel.setVisible(False)
        self.mainLayout.addWidget(self.successGifLabel)

        # ---------- CONNECTIONS ----------
        self.applyButton.clicked.connect(self.onApplyClicked)
        self.cancelButton.clicked.connect(self.close)

    # ---------- SHOW GIF ANIMATION ----------
    def showSuccessGif(self):
        """แสดง GIF ตอน success แล้วซ่อนเองหลังจากเล่นจบ"""
        GIF_PATH = "C:/Users/itobo/OneDrive/เอกสาร/maya/2024/scripts/Final_Project/resourches/image/Happy Jonah Hill GIF.gif"
        GIF_PATH = GIF_PATH.replace("//", "/")  # แก้ path สำหรับ Windows

        if not os.path.exists(GIF_PATH):
            QtWidgets.QMessageBox.warning(self, "GIF not found", f"ไม่พบไฟล์:\n{GIF_PATH}")
            return

        self.successGifLabel.setVisible(True)
        self.successGifLabel.raise_()

        self.movie = QtGui.QMovie(GIF_PATH)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setScaledSize(QtCore.QSize(150, 150))
        self.successGifLabel.setMovie(self.movie)

        if not self.movie.isValid():
            QtWidgets.QMessageBox.warning(self, "Invalid GIF", "โหลดไฟล์ GIF ไม่สำเร็จ")
            return

        self.movie.start()
        self.successGifLabel.show()
        QtWidgets.QApplication.processEvents()  # <--- สำคัญมากสำหรับ Maya

        # ให้ GIF หายไปหลัง 3 วินาที
        QtCore.QTimer.singleShot(3000, self.hideSuccessGif)

    def hideSuccessGif(self):
        self.successGifLabel.setVisible(False)
        if hasattr(self, "movie"):
            self.movie.stop()

    # ---------- APPLY ----------
    def onApplyClicked(self):
        old_name = self.nameLineEdit.text().strip()
        new_name = self.newNameLineEdit.text().strip()
        mode = self.comboBox.currentText()

        if self.hierarchyCheck.isChecked():
            scope = "Hierarchy"
        elif self.selectedCheck.isChecked():
            scope = "Selected"
        else:
            scope = "All"

        try:
            Reui.process(mode, old_name, new_name, scope)
            self.showSuccessGif()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"❌ Failed to process:\n{e}")


def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MyStyleToolDialog(parent=ptr)
    ui.show()
