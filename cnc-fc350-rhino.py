# -*- coding: utf-8 -*-
# ================================================================
# CNC-FC350 Fixed-Column Box-Frame Mill — Rhino 8 Mac
# Working Area: 350 x 300 x 150 mm (X x Y x Z)
# Frame: 6061-T6, CNC Machined, Anodized
# Linear: HGR20 + SFU1605
# All dimensions in mm
# ================================================================
# Coordinate: X=left-right, Y=front-back(+front), Z=up
# Origin: center of base plate bottom surface
# Column at rear (negative Y), operator at front (+Y)
# ================================================================

import Rhino.Geometry as rg
import scriptcontext as sc
import rhinoscriptsyntax as rs
import System.Drawing as SD

# ================================================================
#  DIMENSIONS (mm) — all customizable
# ================================================================

# Working Area
WA_X, WA_Y, WA_Z = 350.0, 300.0, 150.0

# -- A. FRAME PLATES (6061-T6, 25mm thick unless noted) --
BASE_W, BASE_D, BASE_H  = 700.0, 600.0, 25.0      # A1 Base Plate
COL_W_OUTER              = 450.0                     # Column outer width
COL_DEPTH                = 220.0                     # Column depth
COL_HEIGHT               = 520.0                     # Column height
WALL_T                   = 25.0                      # Wall thickness

SADDLE_W, SADDLE_D, SADDLE_H = 480.0, 400.0, 20.0  # A8 Y-Saddle
TABLE_W, TABLE_D, TABLE_H    = 550.0, 380.0, 25.0  # A9 T-slot Table
ZCAR_W, ZCAR_H, ZCAR_T       = 300.0, 260.0, 20.0  # A10 Z-Carriage

# T-slot specs
TSLOT_W, TSLOT_D = 8.5, 12.0   # slot width, depth
TSLOT_PITCH      = 60.0         # slot spacing

# -- B. LINEAR RAILS (HGR20) --
HGR20_W, HGR20_H = 20.0, 27.5  # Rail cross-section
HGH20_W, HGH20_L, HGH20_H = 44.0, 77.5, 30.0  # Block size

Y_RAIL_LEN = 500.0   # Y-axis rail length
Y_RAIL_SEP = 240.0   # Y-axis rail separation
X_RAIL_LEN = 550.0   # X-axis rail length
X_RAIL_SEP = 280.0   # X-axis rail separation
Z_RAIL_LEN = 360.0   # Z-axis rail length
Z_RAIL_SEP = 220.0   # Z-axis rail separation

# -- F. BALL SCREWS (SFU1605) --
BS_SHAFT_R  = 8.0    # Shaft radius (dia 16)
BS_NUT_R    = 14.0   # Nut radius (dia 28)
BS_NUT_L    = 40.0   # Nut length
BK12_R, BK12_L = 19.0, 21.0  # Fixed-end bearing
BF12_R, BF12_L = 15.0, 15.0  # Free-end bearing

Y_BS_LEN = 460.0
X_BS_LEN = 510.0
Z_BS_LEN = 320.0

# -- C. SPINDLE --
SPINDLE_R   = 32.5   # dia 65mm
SPINDLE_LEN = 200.0
CLAMP_R     = 45.0   # Clamp outer radius
CLAMP_H     = 55.0   # Clamp height
ER_R        = 12.0   # ER16 collet radius
ENDMILL_R   = 4.0    # 8mm endmill
ENDMILL_L   = 50.0

# -- D. MOTORS (NEMA23) --
MOTOR_W = 57.0
MOTOR_L = 56.0
SHAFT_R = 3.175  # 6.35mm dia
SHAFT_L = 22.0
COUPLING_R = 12.5
COUPLING_L = 25.0

# -- E. 4th AXIS ROTARY --
ROTARY_BASE_W, ROTARY_BASE_D, ROTARY_BASE_H = 100.0, 100.0, 30.0
CHUCK_R = 40.0   # K11-80, dia 80mm
CHUCK_L = 40.0
TAILSTOCK_W, TAILSTOCK_D, TAILSTOCK_H = 60.0, 60.0, 50.0

# ================================================================
#  COMPUTED POSITIONS (Z stack-up from base)
# ================================================================

# Z stack-up (bottom to top):
Z_BASE_TOP     = BASE_H                              # 25
Z_YRAIL_TOP    = Z_BASE_TOP + HGR20_H                # 52.5
Z_YBLOCK_TOP   = Z_YRAIL_TOP + 16.0                  # 68.5
Z_SADDLE_BOT   = Z_YBLOCK_TOP                        # 68.5
Z_SADDLE_TOP   = Z_SADDLE_BOT + SADDLE_H             # 88.5
Z_XRAIL_TOP    = Z_SADDLE_TOP + HGR20_H              # 116.0
Z_XBLOCK_TOP   = Z_XRAIL_TOP + 16.0                  # 132.0
Z_TABLE_BOT    = Z_XBLOCK_TOP                        # 132.0
Z_TABLE_TOP    = Z_TABLE_BOT + TABLE_H               # 157.0

# Column
COL_Y_BACK     = -BASE_D/2.0                         # -300
COL_Y_FRONT    = COL_Y_BACK + COL_DEPTH              # -80

# Z-carriage mid position (spindle tip at table top + 50mm clearance)
ZCAR_MID_Z     = Z_TABLE_TOP + 100.0 + ZCAR_H/2.0   # ~387

# ================================================================
#  LAYERS
# ================================================================

def make_layer(name, r, g, b):
    if rs.IsLayer(name):
        rs.LayerColor(name, SD.Color.FromArgb(r, g, b))
    else:
        rs.AddLayer(name, SD.Color.FromArgb(r, g, b))
    return name

L = {
    'frame':    make_layer("A_Frame",          148, 163, 184),
    'frame_dk': make_layer("A_Frame_Column",   110, 120, 140),
    'table':    make_layer("A_Table",          176, 184, 196),
    'rail':     make_layer("B_Rail_HGR20",     126, 232, 135),
    'block':    make_layer("B_Block_HGH20CA",   80, 190, 100),
    'screw':    make_layer("F_BallScrew",      121, 192, 255),
    'bearing':  make_layer("F_Bearing",         80, 140, 200),
    'spindle':  make_layer("C_Spindle",        240, 136,  62),
    'clamp':    make_layer("C_Clamp",          200, 110,  48),
    'motor':    make_layer("D_Motor",          227, 179,  65),
    'shaft':    make_layer("D_Shaft",          180, 180, 180),
    'coupling': make_layer("D_Coupling",       170, 170, 170),
    'rotary':   make_layer("E_Rotary",         188, 140, 255),
    'workvol':  make_layer("REF_WorkVolume",    88, 166, 255),
    'gusset':   make_layer("A_Gusset",         130, 140, 155),
    'tslot':    make_layer("A_TSlot",          100, 110, 120),
}

# ================================================================
#  HELPER FUNCTIONS
# ================================================================

def box_brep(x0, y0, z0, x1, y1, z1):
    """Axis-aligned box from (x0,y0,z0) to (x1,y1,z1)"""
    return rg.Box(rg.Plane.WorldXY,
        rg.Interval(min(x0,x1), max(x0,x1)),
        rg.Interval(min(y0,y1), max(y0,y1)),
        rg.Interval(min(z0,z1), max(z0,z1))).ToBrep()

def box_c(cx, cy, cz, sx, sy, sz):
    """Box centered at (cx,cy,cz) with size (sx,sy,sz)"""
    return box_brep(cx-sx/2, cy-sy/2, cz-sz/2, cx+sx/2, cy+sy/2, cz+sz/2)

def cyl_z(cx, cy, z0, z1, r):
    """Cylinder along Z, center (cx,cy), from z0 to z1"""
    pl = rg.Plane(rg.Point3d(cx, cy, z0), rg.Vector3d.ZAxis)
    return rg.Cylinder(rg.Circle(pl, r), abs(z1 - z0)).ToBrep(True, True)

def cyl_y(cx, y0, y1, cz, r):
    """Cylinder along Y, center (cx,cz), from y0 to y1"""
    pl = rg.Plane(rg.Point3d(cx, y0, cz), rg.Vector3d.YAxis)
    return rg.Cylinder(rg.Circle(pl, r), abs(y1 - y0)).ToBrep(True, True)

def cyl_x(x0, x1, cy, cz, r):
    """Cylinder along X, center (cy,cz), from x0 to x1"""
    pl = rg.Plane(rg.Point3d(x0, cy, cz), rg.Vector3d.XAxis)
    return rg.Cylinder(rg.Circle(pl, r), abs(x1 - x0)).ToBrep(True, True)

def add(brep, layer, name=""):
    """Add brep to document on layer with optional name"""
    if brep is None:
        return None
    oid = sc.doc.Objects.AddBrep(brep)
    if oid:
        obj = sc.doc.Objects.Find(oid)
        if obj:
            attr = obj.Attributes
            li = sc.doc.Layers.FindByFullPath(layer, -1)
            if li >= 0:
                attr.LayerIndex = li
            if name:
                attr.Name = name
            obj.CommitChanges()
    return oid

def add_dot(x, y, z, text):
    """Add text dot for labeling"""
    rs.AddTextDot(text, (x, y, z))

# ================================================================
#  CLEANUP
# ================================================================
rs.EnableRedraw(False)
all_objs = rs.AllObjects()
if all_objs:
    rs.DeleteObjects(all_objs)

# ================================================================
#  A. FRAME — 6061-T6 Aluminum
# ================================================================

# A1. Base Plate: 700 x 600 x 25 mm
add(box_c(0, 0, BASE_H/2, BASE_W, BASE_D, BASE_H),
    L['frame'], "A1 Base Plate 700x600x25")

# Column Y positions
bw_cy = COL_Y_BACK + WALL_T/2              # back wall center Y
lw_cx = -(COL_W_OUTER/2 - WALL_T/2)        # left wall center X
rw_cx = COL_W_OUTER/2 - WALL_T/2           # right wall center X
col_cy = COL_Y_BACK + COL_DEPTH/2           # column center Y
col_cz = BASE_H + COL_HEIGHT/2              # column center Z

# A2. Column Back Wall: 450 x 25 x 520 mm
add(box_c(0, bw_cy, col_cz, COL_W_OUTER, WALL_T, COL_HEIGHT),
    L['frame_dk'], "A2 Column Back Wall 450x25x520")

# A3. Column Left Wall: 25 x 220 x 520 mm
add(box_c(lw_cx, col_cy, col_cz, WALL_T, COL_DEPTH, COL_HEIGHT),
    L['frame_dk'], "A3 Column Left Wall 25x220x520")

# A4. Column Right Wall: 25 x 220 x 520 mm
add(box_c(rw_cx, col_cy, col_cz, WALL_T, COL_DEPTH, COL_HEIGHT),
    L['frame_dk'], "A4 Column Right Wall 25x220x520")

# A5. Column Top Plate: 450 x 220 x 25 mm
col_top_z = BASE_H + COL_HEIGHT + WALL_T/2
add(box_c(0, col_cy, col_top_z, COL_W_OUTER, COL_DEPTH, WALL_T),
    L['frame_dk'], "A5 Column Top Plate 450x220x25")

# A6. Gusset Reinforcements (8 pieces — 4 bottom, 4 top)
GUSSET_S = 60.0   # gusset leg length
GUSSET_T = 20.0   # gusset thickness
gusset_xs = [lw_cx, rw_cx]
gusset_ys = [COL_Y_BACK + WALL_T, COL_Y_FRONT - WALL_T]

for i, gx in enumerate(gusset_xs):
    for j, gy in enumerate(gusset_ys):
        # Bottom gussets (base to column)
        add(box_c(gx, gy, BASE_H + GUSSET_S/2, GUSSET_T, GUSSET_T, GUSSET_S),
            L['gusset'], "A6 Gusset Bottom #%d" % (i*2+j+1))
        # Top gussets (column to top plate)
        add(box_c(gx, gy, BASE_H + COL_HEIGHT - GUSSET_S/2, GUSSET_T, GUSSET_T, GUSSET_S),
            L['gusset'], "A6 Gusset Top #%d" % (i*2+j+1))

# A7. Leveling Feet (4 corners of base)
FOOT_R, FOOT_H = 20.0, 15.0
foot_positions = [
    ( BASE_W/2-40,  BASE_D/2-40),
    (-BASE_W/2+40,  BASE_D/2-40),
    ( BASE_W/2-40, -BASE_D/2+40),
    (-BASE_W/2+40, -BASE_D/2+40),
]
for i, (fx, fy) in enumerate(foot_positions):
    add(cyl_z(fx, fy, -FOOT_H, 0, FOOT_R),
        L['frame'], "A7 Leveling Foot #%d" % (i+1))

# ================================================================
#  Y-AXIS (front-back, along Y direction)
#  Rails on base, moves saddle
# ================================================================

# B1. Y-axis HGR20 Rails (2, on base top, running in Y)
yr_z = Z_BASE_TOP  # rail bottom at base top
for sign, side in [(-1, "L"), (1, "R")]:
    rx = sign * Y_RAIL_SEP/2
    add(box_c(rx, 0, yr_z + HGR20_H/2, HGR20_W, Y_RAIL_LEN, HGR20_H),
        L['rail'], "B1 HGR20 Y-Rail %s (500mm)" % side)

# Y-axis HGH20CA Blocks (4, on rails)
yb_z = Z_YRAIL_TOP + HGH20_H/2 - HGR20_H/2  # block center Z
y_block_ys = [-Y_RAIL_LEN/4, Y_RAIL_LEN/4]
idx = 1
for sign in [-1, 1]:
    for yy in y_block_ys:
        add(box_c(sign * Y_RAIL_SEP/2, yy, yr_z + HGR20_H + 8,
                  HGH20_W, HGH20_L, HGH20_H - HGR20_H),
            L['block'], "B1 HGH20CA Y-Block #%d" % idx)
        idx += 1

# F1. Y-axis Ball Screw SFU1605 (460mm)
ybs_z = Z_BASE_TOP + 15.0  # ball screw center Z
add(cyl_y(0, -Y_BS_LEN/2, Y_BS_LEN/2, ybs_z, BS_SHAFT_R),
    L['screw'], "F1 SFU1605 Y-Screw Shaft (460mm)")
# Nut
add(cyl_y(0, -BS_NUT_L/2, BS_NUT_L/2, ybs_z, BS_NUT_R),
    L['screw'], "F1 Y-Screw Nut")
# BK12 (fixed end, rear)
add(cyl_y(0, -Y_BS_LEN/2-BK12_L, -Y_BS_LEN/2, ybs_z, BK12_R),
    L['bearing'], "F1 BK12 Y Fixed-End")
# BF12 (free end, front)
add(cyl_y(0, Y_BS_LEN/2, Y_BS_LEN/2+BF12_L, ybs_z, BF12_R),
    L['bearing'], "F1 BF12 Y Free-End")

# A8. Y-Saddle Plate: 480 x 400 x 20 mm
add(box_c(0, 0, Z_SADDLE_BOT + SADDLE_H/2, SADDLE_W, SADDLE_D, SADDLE_H),
    L['frame'], "A8 Y-Saddle Plate 480x400x20")

# ================================================================
#  X-AXIS (left-right, along X direction)
#  Rails on saddle, moves table
# ================================================================

# B2. X-axis HGR20 Rails (2, on saddle top, running in X)
xr_z = Z_SADDLE_TOP
for sign, side in [(-1, "F"), (1, "R")]:
    ry = sign * X_RAIL_SEP/2
    add(box_c(0, ry, xr_z + HGR20_H/2, X_RAIL_LEN, HGR20_W, HGR20_H),
        L['rail'], "B2 HGR20 X-Rail %s (550mm)" % side)

# X-axis Blocks (4)
idx = 1
x_block_xs = [-X_RAIL_LEN/4, X_RAIL_LEN/4]
for sign in [-1, 1]:
    for xx in x_block_xs:
        add(box_c(xx, sign * X_RAIL_SEP/2, xr_z + HGR20_H + 8,
                  HGH20_L, HGH20_W, HGH20_H - HGR20_H),
            L['block'], "B2 HGH20CA X-Block #%d" % idx)
        idx += 1

# F2. X-axis Ball Screw SFU1605 (510mm)
xbs_z = Z_SADDLE_TOP + 15.0
add(cyl_x(-X_BS_LEN/2, X_BS_LEN/2, 0, xbs_z, BS_SHAFT_R),
    L['screw'], "F2 SFU1605 X-Screw Shaft (510mm)")
add(cyl_x(-BS_NUT_L/2, BS_NUT_L/2, 0, xbs_z, BS_NUT_R),
    L['screw'], "F2 X-Screw Nut")
add(cyl_x(-X_BS_LEN/2-BK12_L, -X_BS_LEN/2, 0, xbs_z, BK12_R),
    L['bearing'], "F2 BK12 X Fixed-End")
add(cyl_x(X_BS_LEN/2, X_BS_LEN/2+BF12_L, 0, xbs_z, BF12_R),
    L['bearing'], "F2 BF12 X Free-End")

# A9. T-Slot Table: 550 x 380 x 25 mm
add(box_c(0, 0, Z_TABLE_BOT + TABLE_H/2, TABLE_W, TABLE_D, TABLE_H),
    L['table'], "A9 T-Slot Table 550x380x25")

# T-Slot grooves (visual)
n_slots = int(TABLE_D / TSLOT_PITCH)
for i in range(n_slots + 1):
    sy = -TABLE_D/2 + 40 + i * TSLOT_PITCH
    if abs(sy) < TABLE_D/2 - 20:
        add(box_c(0, sy, Z_TABLE_TOP - TSLOT_D/2, TABLE_W - 20, TSLOT_W, TSLOT_D),
            L['tslot'], "A9 T-Slot #%d" % (i+1))

# ================================================================
#  Z-AXIS (vertical, along Z direction)
#  Rails on column front face, moves spindle
# ================================================================

# Z-rails mount on the FRONT face of the back wall
zr_y = COL_Y_BACK + WALL_T + 1.0  # just in front of back wall inner face

# B3. Z-axis HGR20 Rails (2, vertical, on column)
zr_z_center = BASE_H + COL_HEIGHT/2 + 20  # slightly above column center
for sign, side in [(-1, "L"), (1, "R")]:
    rx = sign * Z_RAIL_SEP/2
    add(box_c(rx, zr_y + HGR20_H/2, zr_z_center, HGR20_W, HGR20_H, Z_RAIL_LEN),
        L['rail'], "B3 HGR20 Z-Rail %s (360mm)" % side)

# Z-axis Blocks (4)
idx = 1
zb_offsets = [-ZCAR_H/4, ZCAR_H/4]
for sign in [-1, 1]:
    for dz in zb_offsets:
        add(box_c(sign * Z_RAIL_SEP/2, zr_y + HGR20_H + 8,
                  ZCAR_MID_Z + dz,
                  HGH20_W, HGH20_H - HGR20_H, HGH20_L),
            L['block'], "B3 HGH20CA Z-Block #%d" % idx)
        idx += 1

# F3. Z-axis Ball Screw SFU1605 (320mm)
zbs_y = zr_y + 15
add(cyl_z(0, zbs_y, zr_z_center - Z_BS_LEN/2, zr_z_center + Z_BS_LEN/2, BS_SHAFT_R),
    L['screw'], "F3 SFU1605 Z-Screw Shaft (320mm)")
add(cyl_z(0, zbs_y, ZCAR_MID_Z - BS_NUT_L/2, ZCAR_MID_Z + BS_NUT_L/2, BS_NUT_R),
    L['screw'], "F3 Z-Screw Nut")
add(cyl_z(0, zbs_y, zr_z_center + Z_BS_LEN/2, zr_z_center + Z_BS_LEN/2 + BK12_L, BK12_R),
    L['bearing'], "F3 BK12 Z Fixed-End (Top)")
add(cyl_z(0, zbs_y, zr_z_center - Z_BS_LEN/2 - BF12_L, zr_z_center - Z_BS_LEN/2, BF12_R),
    L['bearing'], "F3 BF12 Z Free-End (Bottom)")

# A10. Z-Carriage Plate: 300 x 20 x 260 mm
zcar_y = zr_y + HGR20_H + 20 + ZCAR_T/2
add(box_c(0, zcar_y, ZCAR_MID_Z, ZCAR_W, ZCAR_T, ZCAR_H),
    L['frame'], "A10 Z-Carriage Plate 300x20x260")

# ================================================================
#  C. SPINDLE SYSTEM — 1.5kW Water-Cooled ER16
# ================================================================

sp_y = zcar_y + ZCAR_T/2 + CLAMP_H/2 + 5  # in front of carriage
sp_z = ZCAR_MID_Z - 20  # spindle center, slightly below carriage center

# C1. Spindle Mount Plate
add(box_c(0, zcar_y + ZCAR_T/2 + 8, sp_z, 120, 16, 120),
    L['clamp'], "C1 Spindle Mount Plate")

# C2. 65mm Spindle Clamp
add(cyl_z(0, sp_y, sp_z - CLAMP_H/2, sp_z + CLAMP_H/2, CLAMP_R),
    L['clamp'], "C2 65mm Spindle Clamp")

# C3. Spindle Body (1.5kW, dia 65, length 200)
add(cyl_z(0, sp_y, sp_z - SPINDLE_LEN/2, sp_z + SPINDLE_LEN/2, SPINDLE_R),
    L['spindle'], "C3 Spindle 1.5kW ER16 (65x200mm)")

# C4. ER16 Collet (bottom)
er_z = sp_z - SPINDLE_LEN/2
add(cyl_z(0, sp_y, er_z - 15, er_z, ER_R),
    L['spindle'], "C4 ER16 Collet")

# C5. Endmill
em_z = er_z - 15
add(cyl_z(0, sp_y, em_z - ENDMILL_L, em_z, ENDMILL_R),
    L['shaft'], "C5 Endmill 8mm")

# ================================================================
#  D. MOTORS — NEMA23 3.0Nm x4
# ================================================================

# D1. Y-axis Motor (rear of base)
ym_y = -Y_BS_LEN/2 - BK12_L - COUPLING_L - MOTOR_L/2
add(box_c(0, ym_y, ybs_z, MOTOR_W, MOTOR_L, MOTOR_W),
    L['motor'], "D1 NEMA23 Y-Motor (3.0Nm)")
add(cyl_y(0, ym_y + MOTOR_L/2, ym_y + MOTOR_L/2 + SHAFT_L, ybs_z, SHAFT_R),
    L['shaft'], "D1 Y-Motor Shaft")
# Coupling
add(cyl_y(0, -Y_BS_LEN/2 - BK12_L - COUPLING_L, -Y_BS_LEN/2 - BK12_L, ybs_z, COUPLING_R),
    L['coupling'], "D1 Y-Coupling 8x10")

# D2. X-axis Motor (left side of saddle)
xm_x = -X_BS_LEN/2 - BK12_L - COUPLING_L - MOTOR_L/2
add(box_c(xm_x, 0, xbs_z, MOTOR_L, MOTOR_W, MOTOR_W),
    L['motor'], "D2 NEMA23 X-Motor (3.0Nm)")
add(cyl_x(xm_x + MOTOR_L/2, xm_x + MOTOR_L/2 + SHAFT_L, 0, xbs_z, SHAFT_R),
    L['shaft'], "D2 X-Motor Shaft")
add(cyl_x(-X_BS_LEN/2 - BK12_L - COUPLING_L, -X_BS_LEN/2 - BK12_L, 0, xbs_z, COUPLING_R),
    L['coupling'], "D2 X-Coupling 8x10")

# D3. Z-axis Motor (top of column)
zm_z = col_top_z + WALL_T/2 + COUPLING_L + MOTOR_L/2
add(box_c(0, zbs_y, zm_z, MOTOR_W, MOTOR_W, MOTOR_L),
    L['motor'], "D3 NEMA23 Z-Motor (3.0Nm)")
add(cyl_z(0, zbs_y, col_top_z + WALL_T/2, col_top_z + WALL_T/2 + SHAFT_L, SHAFT_R),
    L['shaft'], "D3 Z-Motor Shaft")
add(cyl_z(0, zbs_y, zr_z_center + Z_BS_LEN/2 + BK12_L,
          zr_z_center + Z_BS_LEN/2 + BK12_L + COUPLING_L, COUPLING_R),
    L['coupling'], "D3 Z-Coupling 8x10")

# ================================================================
#  E. 4TH AXIS ROTARY — K11-80 + Tailstock
# ================================================================

# Rotary on right side of table
rot_x = 100.0
rot_z = Z_TABLE_TOP

# E1. Rotary Base
add(box_c(rot_x, 0, rot_z + ROTARY_BASE_H/2,
          ROTARY_BASE_W, ROTARY_BASE_D, ROTARY_BASE_H),
    L['rotary'], "E1 Rotary Base (A-axis)")

# E2. K11-80 Chuck (along X axis)
chuck_z = rot_z + ROTARY_BASE_H + CHUCK_R
add(cyl_x(rot_x - CHUCK_L/2, rot_x + CHUCK_L/2, 0, chuck_z, CHUCK_R),
    L['rotary'], "E2 K11-80 3-Jaw Chuck (dia 80mm)")

# E3. Tailstock (left side)
ts_x = -120.0
add(box_c(ts_x, 0, rot_z + TAILSTOCK_H/2,
          TAILSTOCK_W, TAILSTOCK_D, TAILSTOCK_H),
    L['rotary'], "E3 Tailstock MT2")
# Tailstock center point
add(cyl_x(ts_x + TAILSTOCK_W/2, rot_x - CHUCK_L/2, 0, chuck_z, 3.0),
    L['shaft'], "E3 Tailstock Center")

# E4. A-axis Motor
add(box_c(rot_x + CHUCK_L/2 + COUPLING_L + MOTOR_L/2, 0, chuck_z,
          MOTOR_L, MOTOR_W*0.85, MOTOR_W*0.85),
    L['motor'], "D4 NEMA23 A-Motor (3.0Nm)")

# ================================================================
#  REF: WORKING VOLUME (transparent reference box)
# ================================================================

wv_z = Z_TABLE_TOP + WA_Z/2 + 5  # 5mm above table
add(box_c(0, 0, wv_z, WA_X, WA_Y, WA_Z),
    L['workvol'], "REF Working Volume 350x300x150mm")

# ================================================================
#  TEXT DOTS — Key dimension labels
# ================================================================

add_dot(0, 0, -30, "CNC-FC350 | 350x300x150mm | Fixed-Column Box Frame")
add_dot(0, BASE_D/2 + 30, Z_TABLE_TOP, "Table Top Z=%.0f" % Z_TABLE_TOP)
add_dot(BASE_W/2 + 20, 0, BASE_H/2, "X -->")
add_dot(0, BASE_D/2 + 20, BASE_H/2, "Y --> (Operator)")
add_dot(-BASE_W/2 - 30, 0, BASE_H + COL_HEIGHT/2, "Z ^")
add_dot(0, 0, wv_z + WA_Z/2 + 10, "Work Volume: 350x300x150mm")

# ================================================================
#  FINISH
# ================================================================

rs.EnableRedraw(True)
rs.ZoomExtents()

print("=" * 60)
print("  CNC-FC350 Fixed-Column Box-Frame Mill")
print("  Working Area: 350 x 300 x 150 mm")
print("  Components generated successfully!")
print("  Layers: %d" % len(L))
print("=" * 60)
print("")
print("  Z Stack-up:")
print("    Base top:    Z = %.1f mm" % Z_BASE_TOP)
print("    Y-rail top:  Z = %.1f mm" % Z_YRAIL_TOP)
print("    Saddle top:  Z = %.1f mm" % Z_SADDLE_TOP)
print("    X-rail top:  Z = %.1f mm" % Z_XRAIL_TOP)
print("    Table top:   Z = %.1f mm" % Z_TABLE_TOP)
print("    Z-carriage:  Z = %.1f mm (mid)" % ZCAR_MID_Z)
print("")
print("  Frame plates: A1~A10 (10 plates)")
print("  HGR20 rails: 6 (2 per axis)")
print("  HGH20CA blocks: 12 (4 per axis)")
print("  SFU1605 screws: 3 (XYZ)")
print("  NEMA23 motors: 4 (XYZ+A)")
print("=" * 60)
