try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from maya import cmds

# ✅ แก้ชื่อ module ให้ตรงกับไฟล์ util ที่คุณมี (เช่น RenameToolUtil.py)
import importlib
from . import RenameToolUtil as Reui
importlib.reload(Reui)


ROOT_RESOURCE_DIR = 'C:/Users/itobo/OneDrive/เอกสาร/maya/2024/scripts/Final_Project/resources'


class MyStyleToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('RENAME TOOL')
        self.resize(340, 480)

        # ---------- MAIN LAYOUT ----------
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet('background-color: #866d68;')

        # ---------- TITLE ----------
        self.titleLabel = QtWidgets.QLabel("RENAME TOOL")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet('''
            QLabel {
                color: white;
                font-size: 26px;
                font-family: "Segoe UI";
                font-weight: bold;
            }
        ''')
        self.mainLayout.addWidget(self.titleLabel)

        # ---------- COMBO BOX ----------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Search and replace name", "Rename", "Prefix hierarchy"])
        self.comboBox.currentIndexChanged.connect(self.index_changed)
        self.mainLayout.addWidget(self.comboBox)
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
            QComboBox QAbstractItemView {
                background-color: #333;
                color: white;
                selection-background-color: #532316;
            }
        ''')

        # ---------- CHECKBOXES (radio style) ----------
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
                QCheckBox::indicator:hover {
                    border: 2px solid #90E0FF;
                }
            ''')
            self.checkboxLayout.addWidget(cb)

        # ---------- SEARCH NAME INPUT ----------
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setPlaceholderText("SEARCH NAME")
        self.nameLineEdit.setStyleSheet('''
            QLineEdit {
                color: black;
                background-color: white;
                font-size: 18px;
                font-weight: bold;
            }
        ''')
        self.mainLayout.addWidget(self.nameLineEdit)

        # ---------- NEW NAME INPUT ----------
        self.newNameLineEdit = QtWidgets.QLineEdit()
        self.newNameLineEdit.setPlaceholderText("NEW NAME")
        self.newNameLineEdit.setStyleSheet('''
            QLineEdit {
                color: black;
                background-color: white;
                font-size: 18px;
                font-weight: bold;
            }
        ''')
        self.mainLayout.addWidget(self.newNameLineEdit)

        # ---------- BUTTONS ----------
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.applyButton = QtWidgets.QPushButton('Apply')
        self.applyButton.setStyleSheet('''
            QPushButton {
                background-color: #af2529;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #57141e;
            }
        ''')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.cancelButton.setStyleSheet('''
            QPushButton {
                background-color: #7a2b0f;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #866c75;
            }
        ''')

        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.mainLayout.addStretch()

        # ---------- CONNECTIONS ----------
        self.applyButton.clicked.connect(self.onApplyClicked)
        self.cancelButton.clicked.connect(self.close)

    # ---------- SIGNAL HANDLERS ----------
    def index_changed(self, i):
        print(f"Index changed to {i}")

    def onApplyClicked(self):
        """เมื่อกด Apply — เรียกใช้ RenameToolUtil"""
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
            QtWidgets.QMessageBox.information(self, "Success", f"✅ Rename process completed!/nMode: {mode}")
            pixmap.setPixmap(QPixmap(f"{IMG_DIR}/boy.png"))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"❌ Failed to process:/n{e}")


def run():
    """Run the UI in Maya"""
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MyStyleToolDialog(parent=ptr)
    ui.show()
