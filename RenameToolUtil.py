import maya.cmds as cmds

from PySide2 import QtCore, QtGui, QtWidgets

# ========================
# 🔹 ปุ่มแบบมีเอฟเฟกต์เฉียง
# ========================
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

        # ---------- เอฟเฟกต์เฉียง ----------
        self.overlay = QtWidgets.QFrame(self)
        self.overlay.setStyleSheet("background-color: #FF723D;")
        self.overlay.setGeometry(-100, 0, 0, self.height())
        self.overlay.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect(self.overlay))
        self.overlay.graphicsEffect().setOpacity(0.5)

        # ตั้งค่า animation
        self.anim = QtCore.QPropertyAnimation(self.overlay, b"geometry")
        self.anim.setDuration(800)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def enterEvent(self, event):
        """เมื่อ hover เข้ามา"""
        self.anim.stop()
        start_rect = QtCore.QRect(-100, 0, 0, self.height())
        end_rect = QtCore.QRect(-20, 0, self.width() + 100, self.height())
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()

        # เปลี่ยนสีตัวอักษร
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
        """เมื่อออกจาก hover"""
        self.anim.stop()
        start_rect = self.overlay.geometry()
        end_rect = QtCore.QRect(-100, 0, 0, self.height())
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()

        # กลับสีข้อความ
        self.setStyleSheet('''
            QPushButton {
                color: #FF723D;
                background-color: transparent;
                border: 2px solid #FF723D;
                text-transform: uppercase;
                font-family: "Aldrich";
                letter-spacing: 2px;
                font-size: 16px;
                font-weight: bold;
            }
        ''')



        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#





def get_target_objects(scope):
    """
    คืนค่ารายชื่อ object ตาม scope ที่เลือก (Hierarchy, Selected, All)
    """
    if scope == "Hierarchy":
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("Please select at least one root object for hierarchy mode.")
            return []
        objs = []
        for s in sel:
            children = cmds.listRelatives(s, allDescendents=True, fullPath=True, type="transform") or []
            objs.extend(children)
            objs.append(s)
        return objs

    elif scope == "Selected":
        sel = cmds.ls(sl=True, long=True, type="transform")
        if not sel:
            cmds.warning("No object selected.")
        return sel

    elif scope == "All":
        all_objs = cmds.ls(dag=True, long=True, type="transform") or []
        system_cameras = {"persp", "top", "front", "side"}
        all_objs = [obj for obj in all_objs if obj.split("|")[-1] not in system_cameras]
        all_objs = list(dict.fromkeys(all_objs))
        return all_objs

    return []


def search_and_replace(search_text, replace_text, targets):
    """แทนที่ข้อความในชื่อ object"""
    if not search_text:
        cmds.warning("Search text cannot be empty.")
        return

    for obj in targets:
        short_name = obj.split("|")[-1]
        if search_text in short_name:
            new_name = short_name.replace(search_text, replace_text)
            try:
                cmds.rename(obj, new_name)
            except:
                cmds.warning(f"Cannot rename: {obj}")


def rename_all(new_name, targets):
    """เปลี่ยนชื่อทั้งหมดตาม new_name โดยเพิ่มเลขต่อท้ายอัตโนมัติ"""
    if not new_name:
        cmds.warning("New name cannot be empty.")
        return

    for i, obj in enumerate(targets, start=1):
        try:
            cmds.rename(obj, f"{new_name}_{i:02d}")
        except:
            cmds.warning(f"Cannot rename: {obj}")


def add_prefix(prefix, targets):
    """เพิ่ม prefix ให้กับชื่อทั้งหมด"""
    if not prefix:
        cmds.warning("Prefix cannot be empty.")
        return

    for obj in targets:
        short_name = obj.split("|")[-1]
        new_name = f"{prefix}{short_name}"
        try:
            cmds.rename(obj, new_name)
        except:
            cmds.warning(f"Cannot rename: {obj}")


def add_suffix(suffix, targets):
    if not suffix:
        cmds.warning("Suffix cannot be empty.")
        return
    for obj in targets:
        short_name = obj.split("|")[-1]
        new_name = f"{short_name}{suffix}"
        try:
            cmds.rename(obj, new_name)
        except:
            cmds.warning(f"Cannot rename: {obj}")


def process(mode, old_name, new_name, scope):
    """ฟังก์ชันหลัก — เรียกตาม mode ที่เลือก"""
    targets = get_target_objects(scope)
    if not targets:
        return

    if mode == "Search and replace name":
        search_and_replace(old_name, new_name, targets)

    elif mode == "Rename":
        rename_all(new_name, targets)

    elif mode == "Prefix":
        add_prefix(new_name, targets)

    elif mode == "Suffix":  # ✅ เพิ่มเงื่อนไขนี้ให้ตรงกับใน UI
        add_suffix(new_name, targets)

    else:
        cmds.warning(f"Unknown mode: {mode}")
