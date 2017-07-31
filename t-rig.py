selected = cmds.ls(selection=True)
if len(selected) != 3:
    cmds.error("Please select only 3 items: front controller, back controller, and vehicle group")

front_locator = None
back_locator = None
vehicle = None

for i, object in reversed(list(enumerate(selected))):
    if front_locator is None and "front" in object.lower():
        front_locator = object
        del selected[i]
        continue
    if back_locator is None and "back" in object.lower():
        back_locator = object
        del selected[i]
        continue
vehicle = selected[0]

if front_locator is None:
    cmds.error("Please select an object with a name containing \"front\"")
if back_locator is None:
    cmds.error("Please select an object with a name containing \"back\"")
if vehicle is None:
    cmds.error("Please select a vehicle group")

cmds.parentConstraint(front_locator, vehicle)
cmds.aimConstraint(back_locator, front_locator)
