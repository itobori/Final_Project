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


from PySide2 import QtCore, QtGui, QtWidgets






#__________________________________________________________________________________#

class MyStyleToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyStyleToolDialog, self).__init__(parent)
        self.setWindowTitle('RENAME TOOL')
        self.resize(550, 450)
        self.setStyleSheet('background-color: 858585;')

        # ---------- MAIN LAYOUT ----------
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        self.setLayout(self.mainLayout)

        # ---------- TITLE ----------
        self.titleLabel = QtWidgets.QLabel("RENAME TOOL")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet('''
            QLabel {
                color: 474747;
                font-size: 18px;
                font-family: "Aldrich";
                font-weight: bold;
            }
        ''')
        self.mainLayout.addWidget(self.titleLabel, 0, 2, 1, 2)

        # ---------- SPINE ANIMATION (GIF) ----------
        self.animLabel = QtWidgets.QLabel()
        self.animLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.mainLayout.addWidget(self.animLabel, 1, 1,QtCore.Qt.AlignLeft) 

        gif_path = r"C:/Users/itobo/OneDrive/เอกสาร/maya/2024/scripts/Final_Project/resourches/image/Benedict Cumberbatch Magic GIF by Spider-Man (1).gif"
        self.movie = QtGui.QMovie(gif_path)

        if not self.movie.isValid():
            print("❌ ไม่พบไฟล์ GIF ที่ระบุ:", gif_path)

        self.animLabel.setMovie(self.movie)
        self.movie.start()






        # ---------- COMBO ----------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["Search and replace name", "Rename", "Prefix","Suffix" ])
        self.comboBox.setStyleSheet('''
            QComboBox {
                background-color: #A1024E;
                color: 474747;
                border-radius: 3px;
                font-size: 16px;
                padding: 4px;
                font-family: "Aldrich";
                font-weight: bold;
            }
            QComboBox:hover {
                background-color: #FF5C8F;
            }
        ''')
        self.mainLayout.addWidget(self.comboBox, 0, 2, 2, 2)

        # ---------- RadioButton ----------
        self.RadioButton = QtWidgets.QHBoxLayout()
        self.RadioButton.setAlignment(QtCore.Qt.AlignCenter)

        self.hierarchyCheck = QtWidgets.QRadioButton("Hierarchy")
        self.selectedCheck = QtWidgets.QRadioButton("Selected")
        self.allCheck = QtWidgets.QRadioButton("All")
        

        for cb in [self.hierarchyCheck, self.selectedCheck, self.allCheck]:
            cb.setStyleSheet('''
                RadioButton {
                    font-size: 16px;
                    color: 474747;
                    font-family: "Aldrich";
                    padding: 4px;
                    spacing: 20px;
                }
                QRadioButton::indicator {
                    width: 16px;                   /* ขยายวงกลม */
                    height: 16px;
                }
                QRadioButton::indicator:checked {
                    background-color: #FF5C8F;
                    border: 2px solid 474747;
                    border-radius: 8px;
                }
                QRadioButton::indicator:unchecked {
                    background-color: #444;
                    border: 2px solid #aaa;
                    border-radius: 8px;
                }
                QRadioButton::indicator:hover {
                    border: 2px solid #A1024E;
                }
                
            ''')
            self.RadioButton.addWidget(cb)

        self.mainLayout.addLayout(self.RadioButton, 1, 2, 3, 2)

        # ---------- INPUT ----------

        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setPlaceholderText("SEARCH NAME")
        self.newNameLineEdit = QtWidgets.QLineEdit()
        self.newNameLineEdit.setPlaceholderText("NEW NAME")
        for le in [self.nameLineEdit, self.newNameLineEdit]:
            le.setStyleSheet('''
                QLineEdit {
                    color: white;
                    background-color: 474747;
                    font-family: "Aldrich";
                    font-size: 16px;
                    font-weight: bold;
                }
            ''')
        self.mainLayout.addWidget(self.nameLineEdit, 2, 2, 1, 2)
        self.mainLayout.addWidget(self.newNameLineEdit, 3, 2, 1, 2)

        # ---------- BUTTON ----------
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout, 4, 2, 1, 2)

        self.applyButton = AnimatedButton('Apply')
        self.cancelButton = AnimatedButton('Cancel')
        
        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)


        # ---------- SUCCESS GIF ----------
        self.successGifLabel = QtWidgets.QLabel()
        self.successGifLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.successGifLabel.setVisible(False)
        self.mainLayout.addWidget(self.successGifLabel)

        # # ---------- CONNECTIONS ----------
        self.applyButton.clicked.connect(self.onApplyClicked)
        self.cancelButton.clicked.connect(self.close)

    # ---------- SHOW GIF IN NEW WINDOW ----------
    def showSuccessGif(self):
        """แสดง GIF success ในหน้าต่างใหม่ แล้วปิดอัตโนมัติ"""
        GIF_PATH = "C:/Users/itobo/OneDrive/เอกสาร/maya/2024/scripts/Final_Project/resourches/image/Benedict Cumberbatch Magic GIF by Spider-Man.gif"
        GIF_PATH = GIF_PATH.replace("//", "/")

        if not os.path.exists(GIF_PATH):
            QtWidgets.QMessageBox.warning(self, "GIF not found", f"ไม่พบไฟล์:\n{GIF_PATH}")
            return

        # ---------- สร้างหน้าต่าง popup ----------
        self.gifDialog = QtWidgets.QDialog(self)
        self.gifDialog.setWindowTitle("Success!")
        self.gifDialog.setModal(True)
        self.gifDialog.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        self.gifDialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.gifDialog.setFixedSize(500, 500)

        layout = QtWidgets.QVBoxLayout(self.gifDialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        label = QtWidgets.QLabel()
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        # ---------- โหลด GIF ----------
        movie = QtGui.QMovie(GIF_PATH)
        movie.setCacheMode(QtGui.QMovie.CacheAll)
        movie.setScaledSize(QtCore.QSize(700, 700))
        label.setMovie(movie)
        movie.start()

        # ---------- ตั้งค่าพื้นหลังโปร่งใส ----------
        self.gifDialog.setStyleSheet("""
            QDialog {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 15px;
            }
        """)

        # ---------- ตั้งเวลาให้ปิดเองหลัง 3 วิ ----------
        QtCore.QTimer.singleShot(3000, self.gifDialog.accept)

        # ---------- แสดง popup ----------
        self.gifDialog.exec_()

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
