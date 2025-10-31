import maya.cmds as cmds

def get_target_objects(scope):
  
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
    
    if not search_text:
        cmds.warning("Search text cannot be empty.")
        return

    renamed_count = 0
    for obj in targets:
        short_name = obj.split("|")[-1]
        if search_text in short_name:
            new_name = short_name.replace(search_text, replace_text)
            try:
                cmds.rename(obj, new_name)
                renamed_count += 1
            except Exception as e:
                cmds.warning(f"Cannot rename '{short_name}': {e}")
    print(f"Search and Replace: Renamed {renamed_count} object(s).")


def rename_all(new_name, targets):
    
    if not new_name:
        cmds.warning("New name cannot be empty.")
        return

    for i, obj in enumerate(targets, start=1):
        try:
            cmds.rename(obj, f"{new_name}_{i:02d}")
        except Exception as e:
            short_name = obj.split("|")[-1]
            cmds.warning(f"Cannot rename '{short_name}': {e}")
    print(f"Rename: Renamed {len(targets)} object(s).")


def add_prefix(prefix, targets):
    
    if not prefix:
        cmds.warning("Prefix cannot be empty.")
        return

    for obj in targets:
        short_name = obj.split("|")[-1]
        new_name = f"{prefix}{short_name}"
        try:
            cmds.rename(obj, new_name)
        except Exception as e:
            cmds.warning(f"Cannot rename '{short_name}': {e}")
    print(f"Prefix: Added prefix to {len(targets)} object(s).")


def add_suffix(suffix, targets):
    
    if not suffix:
        cmds.warning("Suffix cannot be empty.")
        return
        
    for obj in targets:
        short_name = obj.split("|")[-1]
        new_name = f"{short_name}{suffix}"
        try:
            cmds.rename(obj, new_name)
        except Exception as e:
            cmds.warning(f"Cannot rename '{short_name}': {e}")
    print(f"Suffix: Added suffix to {len(targets)} object(s).")


def process(mode, old_name, new_name, scope):
    
    targets = get_target_objects(scope)
    if not targets:
        print("No target objects found for the selected scope.")
        return

    if mode == "Search and replace name":
        search_and_replace(old_name, new_name, targets)

    elif mode == "Rename":
        rename_all(new_name, targets)

    elif mode == "Prefix":
        add_prefix(new_name, targets)

    elif mode == "Suffix":
        add_suffix(new_name, targets)

    else:
        cmds.warning(f"Unknown mode: {mode}")
