import maya.cmds as cmds

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
        # ✅ ดึงทุก object ใน Outliner (เฉพาะ transform node)
        all_objs = cmds.ls(dag=True, long=True, type="transform") or []

        # ✅ ตัดกล้องระบบ Maya ออก
        system_cameras = {"persp", "top", "front", "side"}
        all_objs = [obj for obj in all_objs if obj.split("|")[-1] not in system_cameras]

        # ✅ ลบซ้ำกันออก (กัน rename ซ้ำ)
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


def process(mode, old_name, new_name, scope):
    """ฟังก์ชันหลัก — เรียกตาม mode ที่เลือก"""
    targets = get_target_objects(scope)
    if not targets:
        return

    if mode == "Search and replace name":
        search_and_replace(old_name, new_name, targets)
    elif mode == "Rename":
        rename_all(new_name, targets)
    elif mode == "Prefix hierarchy":
        add_prefix(new_name, targets)
    else:
        cmds.warning(f"Unknown mode: {mode}")

