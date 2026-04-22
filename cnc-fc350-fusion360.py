# -*- coding: utf-8 -*-
# ================================================================
# CNC-FC350 Fixed-Column Box-Frame Mill — Fusion 360 Assembly
# Working Area: 350 x 300 x 150 mm (X x Y x Z)
# Frame: 6061-T6, CNC Machined, Anodized
# ================================================================
# Run: Fusion 360 > UTILITIES > Scripts and Add-Ins > Run
# API internal unit: centimeters (1 cm = 10 mm)
# ================================================================

import adsk.core, adsk.fusion, traceback, math

# ================================================================
#  DIMENSIONS (cm — Fusion 360 internal unit)
# ================================================================

# Working Area
WA_X, WA_Y, WA_Z = 35.0, 30.0, 15.0

# Frame Plates
BASE_W, BASE_D, BASE_H = 70.0, 60.0, 2.5
COL_W_OUTER = 45.0
COL_DEPTH = 22.0
COL_HEIGHT = 52.0
WALL_T = 2.5

SADDLE_W, SADDLE_D, SADDLE_H = 48.0, 40.0, 2.0
TABLE_W, TABLE_D, TABLE_H = 55.0, 38.0, 2.5
ZCAR_W, ZCAR_H, ZCAR_T = 30.0, 26.0, 2.0

# HGR20 Rail
HGR20_W, HGR20_H = 2.0, 2.75
HGH20_W, HGH20_L, HGH20_H = 4.4, 7.75, 3.0

# Rail lengths and separations
Y_RAIL_LEN, Y_RAIL_SEP = 50.0, 24.0
X_RAIL_LEN, X_RAIL_SEP = 55.0, 28.0
Z_RAIL_LEN, Z_RAIL_SEP = 36.0, 22.0

# Ball Screw
BS_R, BS_NUT_R, BS_NUT_L = 0.8, 1.4, 4.0
BK12_R, BK12_L = 1.9, 2.1
BF12_R, BF12_L = 1.5, 1.5
Y_BS_LEN, X_BS_LEN, Z_BS_LEN = 46.0, 51.0, 32.0

# Spindle
SPINDLE_R, SPINDLE_LEN = 3.25, 20.0
CLAMP_R, CLAMP_H = 4.5, 5.5
ER_R = 1.2
ENDMILL_R, ENDMILL_L = 0.4, 5.0

# Motors
MOTOR_W, MOTOR_L = 5.7, 5.6
COUPLING_R, COUPLING_L = 1.25, 2.5

# Rotary
ROTARY_BASE, ROTARY_BASE_H = 10.0, 3.0
CHUCK_R, CHUCK_L = 4.0, 4.0
TAILSTOCK_W, TAILSTOCK_H = 6.0, 5.0

# T-Slot
TSLOT_W, TSLOT_D = 0.85, 1.2
TSLOT_PITCH = 6.0

# Hole sizes (radius in cm)
M5_R = 0.25
M6_R = 0.30
M8_R = 0.40
M10_R = 0.55
M5_CB_R = 0.45   # Counterbore Ø9mm
M10_CB_R = 0.90  # Counterbore Ø18mm
DOWEL_R = 0.40   # Ø8mm dowel

# ================================================================
#  Z STACK-UP (cm)
# ================================================================

Z_BASE_TOP   = BASE_H
Z_YRAIL_TOP  = Z_BASE_TOP + HGR20_H
Z_YBLOCK_TOP = Z_YRAIL_TOP + 1.6
Z_SADDLE_BOT = Z_YBLOCK_TOP
Z_SADDLE_TOP = Z_SADDLE_BOT + SADDLE_H
Z_XRAIL_TOP  = Z_SADDLE_TOP + HGR20_H
Z_XBLOCK_TOP = Z_XRAIL_TOP + 1.6
Z_TABLE_BOT  = Z_XBLOCK_TOP
Z_TABLE_TOP  = Z_TABLE_BOT + TABLE_H

COL_Y_BACK  = -BASE_D / 2.0
COL_Y_FRONT = COL_Y_BACK + COL_DEPTH

ZCAR_MID_Z = Z_TABLE_TOP + 10.0 + ZCAR_H / 2.0

# Column wall centers
BW_CY  = COL_Y_BACK + WALL_T / 2.0
LW_CX  = -(COL_W_OUTER / 2.0 - WALL_T / 2.0)
RW_CX  = COL_W_OUTER / 2.0 - WALL_T / 2.0
COL_CY = COL_Y_BACK + COL_DEPTH / 2.0
COL_CZ = BASE_H + COL_HEIGHT / 2.0
COL_TOP_Z = BASE_H + COL_HEIGHT + WALL_T / 2.0

# Z-axis positions
ZR_Y = COL_Y_BACK + WALL_T + 0.1
ZR_Z_CENTER = BASE_H + COL_HEIGHT / 2.0 + 2.0
ZBS_Y = ZR_Y + 1.5
ZCAR_Y = ZR_Y + HGR20_H + 2.0 + ZCAR_T / 2.0

# Ball screw Z positions
YBS_Z = Z_BASE_TOP + 1.5
XBS_Z = Z_SADDLE_TOP + 1.5

# ================================================================
#  COLORS (R, G, B, A)  0-255
# ================================================================

COLORS = {
    'frame':    (148, 163, 184, 255),
    'frame_dk': (110, 120, 140, 255),
    'table':    (176, 184, 196, 255),
    'dimmed':   (200, 205, 215, 200),
    'rail':     (126, 232, 135, 255),
    'block':    ( 80, 190, 100, 255),
    'screw':    (121, 192, 255, 255),
    'bearing':  ( 80, 140, 200, 255),
    'spindle':  (240, 136,  62, 255),
    'clamp':    (200, 110,  48, 255),
    'motor':    (227, 179,  65, 255),
    'shaft':    (180, 180, 180, 255),
    'coupling': (170, 170, 170, 255),
    'rotary':   (188, 140, 255, 255),
    'gusset':   (130, 140, 155, 255),
    'workvol':  ( 88, 166, 255,  30),
    'hole':     (220,  60,  60, 255),
}

# ================================================================
#  HELPER FUNCTIONS
# ================================================================

def set_color(body, r, g, b, a=255):
    """Set body appearance color."""
    try:
        colorProp = body.appearance.appearanceProperties.itemByName('Color')
        if colorProp:
            colorProp.value = adsk.core.Color.create(r, g, b, a)
    except:
        pass

def create_box_component(rootComp, name, cx, cy, cz, sx, sy, sz, color_key):
    """Create a box component centered at (cx, cy, cz) with size (sx, sy, sz)."""
    occ = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = name

    # Sketch on XY plane
    sketch = comp.sketches.add(comp.xYConstructionPlane)
    x0, y0 = cx - sx / 2.0, cy - sy / 2.0
    x1, y1 = cx + sx / 2.0, cy + sy / 2.0
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(x0, y0, 0),
        adsk.core.Point3D.create(x1, y1, 0)
    )

    # Extrude
    prof = sketch.profiles.item(0)
    ext_input = comp.features.extrudeFeatures.createInput(
        prof, adsk.fusion.FeatureOperations.NewBodyFeature)

    z_bot = cz - sz / 2.0
    z_top = cz + sz / 2.0
    ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(sz))
    ext = comp.features.extrudeFeatures.add(ext_input)

    # Move to correct Z position
    body = ext.bodies.item(0)
    if z_bot != 0:
        move_input = comp.features.moveFeatures.createInput2(
            adsk.core.ObjectCollection.create())
        move_input.bodies.add(body)
        transform = adsk.core.Matrix3D.create()
        transform.translation = adsk.core.Vector3D.create(0, 0, z_bot)
        move_input.defineAsTransform(transform)
        comp.features.moveFeatures.add(move_input)

    # Color
    c = COLORS.get(color_key, (180, 180, 180, 255))
    try:
        app = adsk.core.Application.get()
        design = app.activeProduct
        matLib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        if matLib:
            appearances = matLib.appearances
            baseApp = appearances.itemByName('Steel - Satin')
            if not baseApp:
                baseApp = appearances.item(0)
            newApp = design.appearances.addByCopy(baseApp, name + '_color')
            colorProp = newApp.appearanceProperties.itemByName('Color')
            if colorProp:
                colorProp.value = adsk.core.Color.create(c[0], c[1], c[2], c[3])
            body.appearance = newApp
    except:
        pass

    return comp, body, occ


def create_cylinder_component(rootComp, name, cx, cy, z_bot, height, radius, color_key, axis='Z'):
    """Create a cylinder component."""
    occ = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = name

    # Choose construction plane based on axis
    if axis == 'Z':
        sketch = comp.sketches.add(comp.xYConstructionPlane)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cx, cy, 0), radius)
        prof = sketch.profiles.item(0)
        ext_input = comp.features.extrudeFeatures.createInput(
            prof, adsk.fusion.FeatureOperations.NewBodyFeature)
        ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height))
        ext = comp.features.extrudeFeatures.add(ext_input)
        body = ext.bodies.item(0)
        if z_bot != 0:
            move_input = comp.features.moveFeatures.createInput2(adsk.core.ObjectCollection.create())
            move_input.bodies.add(body)
            t = adsk.core.Matrix3D.create()
            t.translation = adsk.core.Vector3D.create(0, 0, z_bot)
            move_input.defineAsTransform(t)
            comp.features.moveFeatures.add(move_input)

    elif axis == 'Y':
        sketch = comp.sketches.add(comp.xZConstructionPlane)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cx, z_bot + height / 2.0, 0), radius)
        prof = sketch.profiles.item(0)
        ext_input = comp.features.extrudeFeatures.createInput(
            prof, adsk.fusion.FeatureOperations.NewBodyFeature)
        ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height))
        ext_input.setDirectionFlip(True)
        ext = comp.features.extrudeFeatures.add(ext_input)
        body = ext.bodies.item(0)
        move_input = comp.features.moveFeatures.createInput2(adsk.core.ObjectCollection.create())
        move_input.bodies.add(body)
        t = adsk.core.Matrix3D.create()
        t.translation = adsk.core.Vector3D.create(0, cy, 0)
        move_input.defineAsTransform(t)
        comp.features.moveFeatures.add(move_input)

    elif axis == 'X':
        sketch = comp.sketches.add(comp.yZConstructionPlane)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(cy, z_bot + height / 2.0, 0), radius)
        prof = sketch.profiles.item(0)
        ext_input = comp.features.extrudeFeatures.createInput(
            prof, adsk.fusion.FeatureOperations.NewBodyFeature)
        ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height))
        ext = comp.features.extrudeFeatures.add(ext_input)
        body = ext.bodies.item(0)
        move_input = comp.features.moveFeatures.createInput2(adsk.core.ObjectCollection.create())
        move_input.bodies.add(body)
        t = adsk.core.Matrix3D.create()
        t.translation = adsk.core.Vector3D.create(cx, 0, 0)
        move_input.defineAsTransform(t)
        comp.features.moveFeatures.add(move_input)

    c = COLORS.get(color_key, (180, 180, 180, 255))
    try:
        app = adsk.core.Application.get()
        design = app.activeProduct
        matLib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        if matLib:
            appearances = matLib.appearances
            baseApp = appearances.itemByName('Steel - Satin')
            if not baseApp:
                baseApp = appearances.item(0)
            newApp = design.appearances.addByCopy(baseApp, name + '_color')
            colorProp = newApp.appearanceProperties.itemByName('Color')
            if colorProp:
                colorProp.value = adsk.core.Color.create(c[0], c[1], c[2], c[3])
            body.appearance = newApp
    except:
        pass

    return comp, body, occ


def add_holes_to_body(comp, body, hole_positions, hole_radius, depth, z_face):
    """Add holes to a body. hole_positions = [(x,y), ...], holes go downward from z_face."""
    try:
        for hx, hy in hole_positions:
            sketch = comp.sketches.add(comp.xYConstructionPlane)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(hx, hy, 0), hole_radius)
            prof = sketch.profiles.item(0)
            ext_input = comp.features.extrudeFeatures.createInput(
                prof, adsk.fusion.FeatureOperations.CutFeature)
            ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(depth))
            ext_input.participantBodies = [body]
            # Direction: from z_face downward
            comp.features.extrudeFeatures.add(ext_input)
    except:
        pass


# ================================================================
#  MAIN
# ================================================================

def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface

    try:
        # New document
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.DirectDesignType
        rootComp = design.rootComponent

        ui.messageBox('CNC-FC350 Assembly generation starting...\n'
                      'This may take 30-60 seconds.')

        # ==============================================================
        #  A. FRAME PLATES
        # ==============================================================

        # A1. Base Plate
        create_box_component(rootComp, "A1 Base Plate 700x600x25",
            0, 0, BASE_H/2, BASE_W, BASE_D, BASE_H, 'frame')

        # A2. Column Back Wall (dimmed)
        create_box_component(rootComp, "A2 Column Back Wall 450x25x520",
            0, BW_CY, COL_CZ, COL_W_OUTER, WALL_T, COL_HEIGHT, 'dimmed')

        # A3. Column Left Wall
        create_box_component(rootComp, "A3 Column Left Wall 25x220x520",
            LW_CX, COL_CY, COL_CZ, WALL_T, COL_DEPTH, COL_HEIGHT, 'frame_dk')

        # A4. Column Right Wall
        create_box_component(rootComp, "A4 Column Right Wall 25x220x520",
            RW_CX, COL_CY, COL_CZ, WALL_T, COL_DEPTH, COL_HEIGHT, 'frame_dk')

        # A5. Column Top Plate (dimmed)
        create_box_component(rootComp, "A5 Column Top Plate 450x220x25",
            0, COL_CY, COL_TOP_Z, COL_W_OUTER, COL_DEPTH, WALL_T, 'dimmed')

        # A6. Gussets (8)
        GUSSET_S, GUSSET_T2 = 6.0, 2.0
        gi = 1
        for gx in [LW_CX, RW_CX]:
            for gy in [COL_Y_BACK + WALL_T, COL_Y_FRONT - WALL_T]:
                create_box_component(rootComp, "A6 Gusset Bot #%d" % gi,
                    gx, gy, BASE_H + GUSSET_S/2, GUSSET_T2, GUSSET_T2, GUSSET_S, 'gusset')
                create_box_component(rootComp, "A6 Gusset Top #%d" % gi,
                    gx, gy, BASE_H + COL_HEIGHT - GUSSET_S/2, GUSSET_T2, GUSSET_T2, GUSSET_S, 'gusset')
                gi += 1

        # A7. Leveling Feet
        for i, (fx, fy) in enumerate([
            (BASE_W/2-4, BASE_D/2-4), (-BASE_W/2+4, BASE_D/2-4),
            (BASE_W/2-4, -BASE_D/2+4), (-BASE_W/2+4, -BASE_D/2+4)]):
            create_cylinder_component(rootComp, "A7 Leveling Foot #%d" % (i+1),
                fx, fy, -1.5, 1.5, 2.0, 'frame', 'Z')

        # A8. Y-Saddle
        create_box_component(rootComp, "A8 Y-Saddle 480x400x20",
            0, 0, Z_SADDLE_BOT + SADDLE_H/2, SADDLE_W, SADDLE_D, SADDLE_H, 'frame')

        # A9. T-Slot Table
        create_box_component(rootComp, "A9 T-Slot Table 550x380x25",
            0, 0, Z_TABLE_BOT + TABLE_H/2, TABLE_W, TABLE_D, TABLE_H, 'table')

        # A10. Z-Carriage
        create_box_component(rootComp, "A10 Z-Carriage 300x20x260",
            0, ZCAR_Y, ZCAR_MID_Z, ZCAR_W, ZCAR_T, ZCAR_H, 'frame')

        # ==============================================================
        #  B. LINEAR RAILS — HGR20
        # ==============================================================

        # B1. Y-Rails (2)
        yr_z = Z_BASE_TOP
        for sign, side in [(-1, "L"), (1, "R")]:
            create_box_component(rootComp, "B1 HGR20 Y-Rail %s" % side,
                sign * Y_RAIL_SEP/2, 0, yr_z + HGR20_H/2,
                HGR20_W, Y_RAIL_LEN, HGR20_H, 'rail')

        # Y-Blocks (4)
        idx = 1
        for sx in [-1, 1]:
            for yy in [-Y_RAIL_LEN/4, Y_RAIL_LEN/4]:
                create_box_component(rootComp, "B1 HGH20CA Y-Block #%d" % idx,
                    sx * Y_RAIL_SEP/2, yy, yr_z + HGR20_H + 0.8,
                    HGH20_W, HGH20_L, HGH20_H - HGR20_H, 'block')
                idx += 1

        # B2. X-Rails (2)
        xr_z = Z_SADDLE_TOP
        for sign, side in [(-1, "F"), (1, "R")]:
            create_box_component(rootComp, "B2 HGR20 X-Rail %s" % side,
                0, sign * X_RAIL_SEP/2, xr_z + HGR20_H/2,
                X_RAIL_LEN, HGR20_W, HGR20_H, 'rail')

        # X-Blocks (4)
        idx = 1
        for sy in [-1, 1]:
            for xx in [-X_RAIL_LEN/4, X_RAIL_LEN/4]:
                create_box_component(rootComp, "B2 HGH20CA X-Block #%d" % idx,
                    xx, sy * X_RAIL_SEP/2, xr_z + HGR20_H + 0.8,
                    HGH20_L, HGH20_W, HGH20_H - HGR20_H, 'block')
                idx += 1

        # B3. Z-Rails (2)
        for sign, side in [(-1, "L"), (1, "R")]:
            create_box_component(rootComp, "B3 HGR20 Z-Rail %s" % side,
                sign * Z_RAIL_SEP/2, ZR_Y + HGR20_H/2, ZR_Z_CENTER,
                HGR20_W, HGR20_H, Z_RAIL_LEN, 'rail')

        # Z-Blocks (4)
        idx = 1
        for sx in [-1, 1]:
            for dz in [-ZCAR_H/4, ZCAR_H/4]:
                create_box_component(rootComp, "B3 HGH20CA Z-Block #%d" % idx,
                    sx * Z_RAIL_SEP/2, ZR_Y + HGR20_H + 0.8, ZCAR_MID_Z + dz,
                    HGH20_W, HGH20_H - HGR20_H, HGH20_L, 'block')
                idx += 1

        # ==============================================================
        #  F. BALL SCREWS — SFU1605
        # ==============================================================

        # F1. Y Ball Screw
        create_cylinder_component(rootComp, "F1 SFU1605 Y-Shaft",
            0, -Y_BS_LEN/2, YBS_Z, Y_BS_LEN, BS_R, 'screw', 'Y')
        create_cylinder_component(rootComp, "F1 Y-Nut",
            0, -BS_NUT_L/2, YBS_Z, BS_NUT_L, BS_NUT_R, 'screw', 'Y')
        create_cylinder_component(rootComp, "F1 BK12 Y",
            0, -Y_BS_LEN/2 - BK12_L, YBS_Z, BK12_L, BK12_R, 'bearing', 'Y')
        create_cylinder_component(rootComp, "F1 BF12 Y",
            0, Y_BS_LEN/2, YBS_Z, BF12_L, BF12_R, 'bearing', 'Y')

        # F2. X Ball Screw
        create_cylinder_component(rootComp, "F2 SFU1605 X-Shaft",
            -X_BS_LEN/2, 0, XBS_Z, X_BS_LEN, BS_R, 'screw', 'X')
        create_cylinder_component(rootComp, "F2 X-Nut",
            -BS_NUT_L/2, 0, XBS_Z, BS_NUT_L, BS_NUT_R, 'screw', 'X')
        create_cylinder_component(rootComp, "F2 BK12 X",
            -X_BS_LEN/2 - BK12_L, 0, XBS_Z, BK12_L, BK12_R, 'bearing', 'X')
        create_cylinder_component(rootComp, "F2 BF12 X",
            X_BS_LEN/2, 0, XBS_Z, BF12_L, BF12_R, 'bearing', 'X')

        # F3. Z Ball Screw
        create_cylinder_component(rootComp, "F3 SFU1605 Z-Shaft",
            0, ZBS_Y, ZR_Z_CENTER - Z_BS_LEN/2, Z_BS_LEN, BS_R, 'screw', 'Z')
        create_cylinder_component(rootComp, "F3 Z-Nut",
            0, ZBS_Y, ZCAR_MID_Z - BS_NUT_L/2, BS_NUT_L, BS_NUT_R, 'screw', 'Z')
        create_cylinder_component(rootComp, "F3 BK12 Z",
            0, ZBS_Y, ZR_Z_CENTER + Z_BS_LEN/2, BK12_L, BK12_R, 'bearing', 'Z')
        create_cylinder_component(rootComp, "F3 BF12 Z",
            0, ZBS_Y, ZR_Z_CENTER - Z_BS_LEN/2 - BF12_L, BF12_L, BF12_R, 'bearing', 'Z')

        # ==============================================================
        #  C. SPINDLE SYSTEM
        # ==============================================================

        sp_y = ZCAR_Y + ZCAR_T/2 + CLAMP_H/2 + 0.5
        sp_z = ZCAR_MID_Z - 2.0

        # C1. Spindle Mount Plate
        create_box_component(rootComp, "C1 Spindle Mount Plate",
            0, ZCAR_Y + ZCAR_T/2 + 0.8, sp_z, 12.0, 1.6, 12.0, 'clamp')

        # C2. 65mm Clamp
        create_cylinder_component(rootComp, "C2 65mm Clamp",
            0, sp_y, sp_z - CLAMP_H/2, CLAMP_H, CLAMP_R, 'clamp', 'Z')

        # C3. Spindle Body
        create_cylinder_component(rootComp, "C3 Spindle 1.5kW ER16",
            0, sp_y, sp_z - SPINDLE_LEN/2, SPINDLE_LEN, SPINDLE_R, 'spindle', 'Z')

        # C4. ER16 Collet
        create_cylinder_component(rootComp, "C4 ER16 Collet",
            0, sp_y, sp_z - SPINDLE_LEN/2 - 1.5, 1.5, ER_R, 'spindle', 'Z')

        # C5. Endmill
        create_cylinder_component(rootComp, "C5 Endmill 8mm",
            0, sp_y, sp_z - SPINDLE_LEN/2 - 1.5 - ENDMILL_L, ENDMILL_L, ENDMILL_R, 'shaft', 'Z')

        # ==============================================================
        #  D. MOTORS — NEMA23
        # ==============================================================

        # D1. Y-Motor
        ym_y = -Y_BS_LEN/2 - BK12_L - COUPLING_L - MOTOR_L/2
        create_box_component(rootComp, "D1 NEMA23 Y-Motor",
            0, ym_y, YBS_Z, MOTOR_W, MOTOR_L, MOTOR_W, 'motor')
        create_cylinder_component(rootComp, "D1 Y-Coupling",
            0, -Y_BS_LEN/2 - BK12_L - COUPLING_L, YBS_Z, COUPLING_L, COUPLING_R, 'coupling', 'Y')

        # D2. X-Motor
        xm_x = -X_BS_LEN/2 - BK12_L - COUPLING_L - MOTOR_L/2
        create_box_component(rootComp, "D2 NEMA23 X-Motor",
            xm_x, 0, XBS_Z, MOTOR_L, MOTOR_W, MOTOR_W, 'motor')
        create_cylinder_component(rootComp, "D2 X-Coupling",
            -X_BS_LEN/2 - BK12_L - COUPLING_L, 0, XBS_Z, COUPLING_L, COUPLING_R, 'coupling', 'X')

        # D3. Z-Motor
        zm_z = COL_TOP_Z + WALL_T/2 + COUPLING_L + MOTOR_L/2
        create_box_component(rootComp, "D3 NEMA23 Z-Motor",
            0, ZBS_Y, zm_z, MOTOR_W, MOTOR_W, MOTOR_L, 'motor')
        create_cylinder_component(rootComp, "D3 Z-Coupling",
            0, ZBS_Y, COL_TOP_Z + WALL_T/2, COUPLING_L, COUPLING_R, 'coupling', 'Z')

        # ==============================================================
        #  E. 4TH AXIS ROTARY
        # ==============================================================

        rot_x = 10.0
        rot_z = Z_TABLE_TOP

        # E1. Rotary Base
        create_box_component(rootComp, "E1 Rotary Base",
            rot_x, 0, rot_z + ROTARY_BASE_H/2, ROTARY_BASE, ROTARY_BASE, ROTARY_BASE_H, 'rotary')

        # E2. K11-80 Chuck
        create_cylinder_component(rootComp, "E2 K11-80 Chuck",
            rot_x - CHUCK_L/2, 0, rot_z + ROTARY_BASE_H + CHUCK_R,
            CHUCK_L, CHUCK_R, 'rotary', 'X')

        # E3. Tailstock
        ts_x = -12.0
        chuck_z = rot_z + ROTARY_BASE_H + CHUCK_R
        create_box_component(rootComp, "E3 Tailstock MT2",
            ts_x, 0, rot_z + TAILSTOCK_H/2, TAILSTOCK_W, TAILSTOCK_W, TAILSTOCK_H, 'rotary')

        # D4. A-Motor
        create_box_component(rootComp, "D4 NEMA23 A-Motor",
            rot_x + CHUCK_L/2 + COUPLING_L + MOTOR_L/2, 0, chuck_z,
            MOTOR_L, MOTOR_W * 0.85, MOTOR_W * 0.85, 'motor')

        # ==============================================================
        #  WORK VOLUME (transparent box)
        # ==============================================================

        wv_z = Z_TABLE_TOP + WA_Z/2 + 0.5
        create_box_component(rootComp, "REF Work Volume 350x300x150",
            0, 0, wv_z, WA_X, WA_Y, WA_Z, 'workvol')

        # ==============================================================
        #  DONE
        # ==============================================================

        # Fit all
        app.activeViewport.fit()

        ui.messageBox(
            'CNC-FC350 Assembly Generated!\n\n'
            'Components: ~70\n'
            'Table top: Z = %.1f cm (%.0f mm)\n\n'
            'Next steps:\n'
            '1. Insert GrabCAD STEP files (Insert > Mesh)\n'
            '2. Replace simplified parts with real models\n'
            '3. Check interference (Inspect > Interference)\n'
            '4. Generate 2D drawings (Drawing > From Design)'
            % (Z_TABLE_TOP, Z_TABLE_TOP * 10)
        )

    except:
        if ui:
            ui.messageBox('Error:\n{}'.format(traceback.format_exc()))
