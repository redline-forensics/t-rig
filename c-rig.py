curves = cmds.ls(selection=True, type="transform")

if len(curves) == 1:
    front_curve = curves[0]
    back_curve = cmds.duplicate(front_curve, name="{}_back".format(front_curve))[0]
    cmds.move(1, 1, 0, back_curve, relative=True)
elif len(curves) == 2:
    front_curve = None
    back_curve = None
    
    for curve in curves:
        if "front" in curve.lower():
            front_curve = curve
            continue
        if "back" in curve.lower():
            back_curve = curve
            
    if not front_curve:
        cmds.error("No curve with name containing \"front\" selected")
    if not back_curve:
        cmds.error("No curve with name containing \"back\" selected")
else:
    cmds.error("Please select 2 existing curves or 1 curve to duplicate")

front_curve_shape = cmds.listRelatives(front_curve)[0]
cmds.setAttr("{}.overrideEnabled".format(front_curve_shape), True)
cmds.setAttr("{}.overrideColor".format(front_curve_shape), 13)

back_curve_shape = cmds.listRelatives(back_curve)[0]
cmds.setAttr("{}.overrideEnabled".format(back_curve_shape), True)
cmds.setAttr("{}.overrideColor".format(back_curve_shape), 14)

cmds.select(front_curve)
mel.eval("performClosestPointOn 0")
front_master = cmds.rename("cpConstraintIn", "vehicle_controller")
cmds.addAttr(front_master, shortName="vLen", longName="vehicleLength", niceName="Vehicle Length", attributeType="float", keyable=True, storable=True, writable=True, readable=True)
front_slave = cmds.rename("cpConstraintPos", "vehicle_front")
front_slave_point = cmds.listConnections(type="nearestPointOnCurve")[0]

cmds.select(back_curve)
mel.eval("performClosestPointOn 0")
back_master = cmds.rename("cpConstraintIn", "back_master")
back_slave = cmds.rename("cpConstraintPos", "vehicle_back")

motion_path = cmds.pathAnimation(back_master, curve=front_curve)

cmds.disconnectAttr("{mp}_uValue.output".format(mp=motion_path), "{mp}.uValue".format(mp=motion_path))
cmds.expression(string="{mp}.uValue = {fsp}.parameter - {fm}.vehicleLength / `arclen {fc}`".format(mp=motion_path, fsp=front_slave_point, fm=front_master, fc=front_curve))
