try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

ROOT_RESOURCE_DIR = 'C:/Users/itobo/OneDrive/เอกสาร/maya/2024/scripts/myStlyeTool/recouse'


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
        self.titleLabel.setStyleSheet(
            '''
                QLabel {
                    color: white;
                    font-size: 26px;
                    font-family: "Segoe UI";
                    font-weight: bold;
                }
            '''
        )
        self.mainLayout.addWidget(self.titleLabel)

        # ---------- COMBO BOX ----------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Search and replace name", "Rename", "Prefix hierarchy"])
        self.comboBox.currentIndexChanged.connect(self.index_changed)
        self.comboBox.currentTextChanged.connect(self.text_changed)
        self.mainLayout.addWidget(self.comboBox)

        # StyleSheet for ComboBox (เพิ่มตอน hold)
        self.comboBox.setStyleSheet(
            '''
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
                QComboBox:pressed {
                    background-color: #532316;
                }
                QComboBox QAbstractItemView {
                    background-color: #333;
                    color: white;
                    selection-background-color: #532316;
                }
            '''
        )

        # ---------- CHECKBOXES (radio style) ----------
        self.checkboxLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.checkboxLayout)

        self.hierarchyCheck = QtWidgets.QCheckBox("Hierarchy")
        self.selectedCheck = QtWidgets.QCheckBox("Selected")
        self.allCheck = QtWidgets.QCheckBox("All")

        # ตั้งค่าเริ่มต้น
        self.selectedCheck.setChecked(True)

        # สร้าง group ให้เลือกได้ทีละอันเท่านั้น
        self.checkGroup = QtWidgets.QButtonGroup(self)
        self.checkGroup.setExclusive(True)
        for cb in [self.hierarchyCheck, self.selectedCheck, self.allCheck]:
            self.checkGroup.addButton(cb)
            cb.setStyleSheet(
                '''
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
                '''
            )
            cb.stateChanged.connect(self.onCheckStateChanged)
            self.checkboxLayout.addWidget(cb)

        # ---------- SEARCH NAME INPUT ----------
        self.nameLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.nameLayout)
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setPlaceholderText("SEARCH NAME")
        self.nameLineEdit.setStyleSheet(
            '''
                QLineEdit {
                    color: black;
                    background-color: white;
                    font-size: 18px;
                    font-weight: bold;
                }
            '''
        )
        self.nameLayout.addWidget(self.nameLineEdit)

        # ---------- NEW NAME INPUT ----------
        self.newNameLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.newNameLayout)
        self.newNameLineEdit = QtWidgets.QLineEdit()
        self.newNameLineEdit.setPlaceholderText("NEW NAME")
        self.newNameLineEdit.setStyleSheet(
            '''
                QLineEdit {
                    color: black;
                    background-color: white;
                    font-size: 18px;
                    font-weight: bold;
                }
            '''
        )
        self.newNameLayout.addWidget(self.newNameLineEdit)

        # ---------- BUTTONS ----------
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.applyButton = QtWidgets.QPushButton('Apply')
        self.applyButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #af2529;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    padding: 8px;
                    font-family: "Dino Care";
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #57141e;
                }
                QPushButton:pressed {
                    background-color: white;
                }
            '''
        )

        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.cancelButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #7a2b0f;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    padding: 8px;
                    font-family: "Dino Care";
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #866c75;
                }
                QPushButton:pressed {
                    background-color: white;
                }
            '''
        )

        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.mainLayout.addStretch()

        # ---------- CONNECTIONS ----------
        self.applyButton.clicked.connect(self.onApplyClicked)
        self.cancelButton.clicked.connect(self.close)

    # ---------- SIGNAL HANDLERS ----------
    def index_changed(self, i):
        print(f"Index changed to {i}")

    def text_changed(self, s):
        print(f"Text changed to {s}")

    def onCheckStateChanged(self):
        selected = None
        if self.hierarchyCheck.isChecked():
            selected = "Hierarchy"
        elif self.selectedCheck.isChecked():
            selected = "Selected"
        elif self.allCheck.isChecked():
            selected = "All"
        print(f"Active checkbox: {selected}")

    def onApplyClicked(self):
        old_name = self.nameLineEdit.text().strip()
        new_name = self.newNameLineEdit.text().strip()
        mode = self.comboBox.currentText()

        active = None
        if self.hierarchyCheck.isChecked():
            active = "Hierarchy"
        elif self.selectedCheck.isChecked():
            active = "Selected"
        elif self.allCheck.isChecked():
            active = "All"

        msg = f"Mode: {mode}\nSearch: {old_name}\nReplace: {new_name}\nActive Option: {active}"
        print(msg)
        QtWidgets.QMessageBox.information(self, "Apply", msg)


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

        # เรียก util
        Reuitil.process(mode, old_name, new_name, scope)


def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = MyStyleToolDialog(parent=ptr)
    ui.show()

