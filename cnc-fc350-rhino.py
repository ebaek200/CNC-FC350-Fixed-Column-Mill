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

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import System.Drawing as SD

# ================================================================
#  DIMENSIONS (mm)
# ================================================================

WA_X, WA_Y, WA_Z = 350.0, 300.0, 150.0

BASE_W, BASE_D, BASE_H       = 700.0, 600.0, 25.0
COL_W_OUTER                   = 450.0
COL_DEPTH                     = 220.0
COL_HEIGHT                    = 520.0
WALL_T                        = 25.0

SADDLE_W, SADDLE_D, SADDLE_H  = 480.0, 400.0, 20.0
TABLE_W, TABLE_D, TABLE_H     = 550.0, 380.0, 25.0
ZCAR_W, ZCAR_H, ZCAR_T        = 300.0, 260.0, 20.0

TSLOT_W, TSLOT_D              = 8.5, 12.0
TSLOT_PITCH                   = 60.0

HGR20_W, HGR20_H              = 20.0, 27.5
HGH20_W, HGH20_L, HGH20_H    = 44.0, 77.5, 30.0

Y_RAIL_LEN, Y_RAIL_SEP        = 500.0, 240.0
X_RAIL_LEN, X_RAIL_SEP        = 550.0, 280.0
Z_RAIL_LEN, Z_RAIL_SEP        = 360.0, 220.0

BS_R, BS_NUT_R, BS_NUT_L      = 8.0, 14.0, 40.0
BK12_R, BK12_L                = 19.0, 21.0
BF12_R, BF12_L                = 15.0, 15.0

Y_BS_LEN, X_BS_LEN, Z_BS_LEN  = 460.0, 510.0, 320.0

SPINDLE_R, SPINDLE_LEN         = 32.5, 200.0
CLAMP_R, CLAMP_H               = 45.0, 55.0
ER_R, ENDMILL_R, ENDMILL_L     = 12.0, 4.0, 50.0

MOTOR_W, MOTOR_L               = 57.0, 56.0
SHAFT_R, SHAFT_L               = 3.175, 22.0
COUPLING_R, COUPLING_L         = 12.5, 25.0

ROTARY_BASE                    = 100.0
ROTARY_BASE_H                  = 30.0
CHUCK_R, CHUCK_L               = 40.0, 40.0
TAILSTOCK_W                    = 60.0
TAILSTOCK_H                    = 50.0

# ================================================================
#  Z STACK-UP
# ================================================================

Z_BASE_TOP   = BASE_H                              # 25
Z_YRAIL_TOP  = Z_BASE_TOP + HGR20_H                # 52.5
Z_YBLOCK_TOP = Z_YRAIL_TOP + 16.0                  # 68.5
Z_SADDLE_BOT = Z_YBLOCK_TOP                        # 68.5
Z_SADDLE_TOP = Z_SADDLE_BOT + SADDLE_H             # 88.5
Z_XRAIL_TOP  = Z_SADDLE_TOP + HGR20_H              # 116
Z_XBLOCK_TOP = Z_XRAIL_TOP + 16.0                  # 132
Z_TABLE_BOT  = Z_XBLOCK_TOP                        # 132
Z_TABLE_TOP  = Z_TABLE_BOT + TABLE_H               # 157

COL_Y_BACK   = -BASE_D / 2.0                       # -300
COL_Y_FRONT  = COL_Y_BACK + COL_DEPTH              # -80

ZCAR_MID_Z   = Z_TABLE_TOP + 100.0 + ZCAR_H/2.0   # ~387

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
    'dimmed':   make_layer("A_Dimmed",         200, 205, 215),
    'hole':     make_layer("G_MountHoles",     220,  60,  60),
    'dowel':    make_layer("G_DowelPins",      255, 120,  40),
}

# ================================================================
#  HELPERS — rs.AddBox / rs.AddCylinder (음영 모드 정상 표시)
# ================================================================

def box_c(cx, cy, cz, sx, sy, sz, layer, name=""):
    """Box centered at (cx,cy,cz), size (sx,sy,sz)"""
    x0, y0, z0 = cx-sx/2.0, cy-sy/2.0, cz-sz/2.0
    x1, y1, z1 = cx+sx/2.0, cy+sy/2.0, cz+sz/2.0
    pts = [
        (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)
    ]
    oid = rs.AddBox(pts)
    if oid:
        rs.ObjectLayer(oid, layer)
        if name: rs.ObjectName(oid, name)
    return oid

def cyl_z(cx, cy, z_bot, height, radius, layer, name=""):
    """Cylinder along Z"""
    plane = rs.MovePlane(rs.WorldXYPlane(), (cx, cy, z_bot))
    oid = rs.AddCylinder(plane, height, radius, cap=True)
    if oid:
        rs.ObjectLayer(oid, layer)
        if name: rs.ObjectName(oid, name)
    return oid

def cyl_y(cx, y_start, length, cz, radius, layer, name=""):
    """Cylinder along Y"""
    plane = rs.PlaneFromNormal((cx, y_start, cz), (0, 1, 0))
    oid = rs.AddCylinder(plane, length, radius, cap=True)
    if oid:
        rs.ObjectLayer(oid, layer)
        if name: rs.ObjectName(oid, name)
    return oid

def cyl_x(x_start, length, cy, cz, radius, layer, name=""):
    """Cylinder along X"""
    plane = rs.PlaneFromNormal((x_start, cy, cz), (1, 0, 0))
    oid = rs.AddCylinder(plane, length, radius, cap=True)
    if oid:
        rs.ObjectLayer(oid, layer)
        if name: rs.ObjectName(oid, name)
    return oid

def hole_z(cx, cy, z_bot, depth, radius, layer, name=""):
    """Mounting hole indicator (small cylinder) along Z"""
    plane = rs.MovePlane(rs.WorldXYPlane(), (cx, cy, z_bot))
    oid = rs.AddCylinder(plane, depth, radius, cap=True)
    if oid:
        rs.ObjectLayer(oid, layer)
        if name: rs.ObjectName(oid, name)
    return oid

# ================================================================
#  CLEANUP
# ================================================================
rs.EnableRedraw(False)
all_objs = rs.AllObjects()
if all_objs:
    rs.DeleteObjects(all_objs)

# ================================================================
#  A. FRAME — 6061-T6
# ================================================================

# A1. Base Plate
box_c(0, 0, BASE_H/2, BASE_W, BASE_D, BASE_H,
      L['frame'], "A1 Base Plate 700x600x25")

# Column positions
bw_cy  = COL_Y_BACK + WALL_T/2
lw_cx  = -(COL_W_OUTER/2 - WALL_T/2)
rw_cx  = COL_W_OUTER/2 - WALL_T/2
col_cy = COL_Y_BACK + COL_DEPTH/2
col_cz = BASE_H + COL_HEIGHT/2

# A2. Column Back Wall (딤드)
box_c(0, bw_cy, col_cz, COL_W_OUTER, WALL_T, COL_HEIGHT,
      L['dimmed'], "A2 Column Back Wall 450x25x520")

# A3. Column Left Wall
box_c(lw_cx, col_cy, col_cz, WALL_T, COL_DEPTH, COL_HEIGHT,
      L['frame_dk'], "A3 Column Left Wall 25x220x520")

# A4. Column Right Wall
box_c(rw_cx, col_cy, col_cz, WALL_T, COL_DEPTH, COL_HEIGHT,
      L['frame_dk'], "A4 Column Right Wall 25x220x520")

# A5. Column Top Plate (딤드)
col_top_z = BASE_H + COL_HEIGHT + WALL_T/2
box_c(0, col_cy, col_top_z, COL_W_OUTER, COL_DEPTH, WALL_T,
      L['dimmed'], "A5 Column Top Plate 450x220x25")

# A6. Gussets (8)
GUSSET_S, GUSSET_T2 = 60.0, 20.0
gusset_xs = [lw_cx, rw_cx]
gusset_ys = [COL_Y_BACK + WALL_T, COL_Y_FRONT - WALL_T]
gi = 1
for gx in gusset_xs:
    for gy in gusset_ys:
        box_c(gx, gy, BASE_H + GUSSET_S/2, GUSSET_T2, GUSSET_T2, GUSSET_S,
              L['gusset'], "A6 Gusset Bot #%d" % gi)
        box_c(gx, gy, BASE_H + COL_HEIGHT - GUSSET_S/2, GUSSET_T2, GUSSET_T2, GUSSET_S,
              L['gusset'], "A6 Gusset Top #%d" % gi)
        gi += 1

# A7. Leveling Feet
for i, (fx, fy) in enumerate([
    (BASE_W/2-40, BASE_D/2-40), (-BASE_W/2+40, BASE_D/2-40),
    (BASE_W/2-40, -BASE_D/2+40), (-BASE_W/2+40, -BASE_D/2+40)]):
    cyl_z(fx, fy, -15, 15, 20, L['frame'], "A7 Leveling Foot #%d" % (i+1))

# ================================================================
#  A1 MOUNTING HOLES — Base Plate
# ================================================================

HOLE_R_M5  = 2.5
HOLE_R_M6  = 3.0
HOLE_R_M8  = 4.0
HOLE_R_M10 = 5.5
DOWEL_R    = 4.0

# HGR20 Y-Rail bolt holes (M5, 16 holes)
for sx in [-1, 1]:
    rx = sx * Y_RAIL_SEP / 2.0
    for yy in [-220, -160, -100, -40, 20, 80, 140, 200]:
        hole_z(rx, yy, 0, BASE_H, HOLE_R_M5, L['hole'], "H M5 Y-Rail")

# BK12 Y-axis (rear, 2 holes)
for dx in [-16, 16]:
    hole_z(dx, -Y_BS_LEN/2, 0, BASE_H, HOLE_R_M5, L['hole'], "H M5 BK12-Y")

# BF12 Y-axis (front, 2 holes)
for dx in [-16, 16]:
    hole_z(dx, Y_BS_LEN/2, 0, BASE_H, HOLE_R_M5, L['hole'], "H M5 BF12-Y")

# Column Back Wall A2 bolts (M10, 6 holes)
for xx in [-200, -120, -40, 40, 120, 200]:
    hole_z(xx, bw_cy, 0, BASE_H, HOLE_R_M10, L['hole'], "H M10 A2-Base")
# A2 dowel pins
for xx in [-100, 100]:
    hole_z(xx, bw_cy, 0, BASE_H, DOWEL_R, L['dowel'], "H Dowel A2")

# Column Side Wall A3/A4 bolts (M10, 4 per side)
for wx in [lw_cx, rw_cx]:
    for yy in [-270, -230, -150, -110]:
        hole_z(wx, yy, 0, BASE_H, HOLE_R_M10, L['hole'], "H M10 SideWall-Base")
    # Dowel pins
    for yy in [-250, -130]:
        hole_z(wx, yy, 0, BASE_H, DOWEL_R, L['dowel'], "H Dowel SideWall")

# Leveling Feet (M12, 4 holes)
for fx, fy in [(310,260),(-310,260),(310,-260),(-310,-260)]:
    hole_z(fx, fy, -5, 5, 6.0, L['hole'], "H M12 LevFoot")

# ================================================================
#  Y-AXIS
# ================================================================

yr_z = Z_BASE_TOP
ybs_z = Z_BASE_TOP + 15.0

# B1. Y-Rails
for sign, side in [(-1,"L"),(1,"R")]:
    box_c(sign*Y_RAIL_SEP/2, 0, yr_z+HGR20_H/2, HGR20_W, Y_RAIL_LEN, HGR20_H,
          L['rail'], "B1 HGR20 Y-Rail %s" % side)

# Y-Blocks
idx = 1
for sx in [-1, 1]:
    for yy in [-Y_RAIL_LEN/4, Y_RAIL_LEN/4]:
        box_c(sx*Y_RAIL_SEP/2, yy, yr_z+HGR20_H+8,
              HGH20_W, HGH20_L, HGH20_H-HGR20_H,
              L['block'], "B1 HGH20CA Y-Block #%d" % idx)
        idx += 1

# F1. Y Ball Screw
cyl_y(0, -Y_BS_LEN/2, Y_BS_LEN, ybs_z, BS_R, L['screw'], "F1 SFU1605 Y-Shaft")
cyl_y(0, -BS_NUT_L/2, BS_NUT_L, ybs_z, BS_NUT_R, L['screw'], "F1 Y-Nut")
cyl_y(0, -Y_BS_LEN/2-BK12_L, BK12_L, ybs_z, BK12_R, L['bearing'], "F1 BK12 Y")
cyl_y(0, Y_BS_LEN/2, BF12_L, ybs_z, BF12_R, L['bearing'], "F1 BF12 Y")

# A8. Y-Saddle
box_c(0, 0, Z_SADDLE_BOT+SADDLE_H/2, SADDLE_W, SADDLE_D, SADDLE_H,
      L['frame'], "A8 Y-Saddle 480x400x20")

# ================================================================
#  A8 MOUNTING HOLES — Y-Saddle
# ================================================================

# HGH20CA Y-Block tapped holes (M6, 4 per block, 4 blocks = 16)
for sx in [-1, 1]:
    for yy_off in [-Y_RAIL_LEN/4, Y_RAIL_LEN/4]:
        bx = sx * Y_RAIL_SEP / 2.0
        by = yy_off
        for ddx in [-16, 16]:
            for ddy in [-25, 25]:
                hole_z(bx+ddx, by+ddy, Z_SADDLE_BOT, SADDLE_H,
                       HOLE_R_M6, L['hole'], "H M6 Y-Block")

# DSG16H Y-nut (4× M5 + Ø28 bore)
for dx, dy in [(-24, -18), (24, -18), (-24, 18), (24, 18)]:
    hole_z(dx, dy, Z_SADDLE_BOT, SADDLE_H,
           HOLE_R_M5, L['hole'], "H M5 DSG16H-Y")
hole_z(0, 0, Z_SADDLE_BOT, SADDLE_H, 14.0, L['hole'], "H Bore DSG16H-Y")

# ================================================================
#  X-AXIS
# ================================================================

xr_z = Z_SADDLE_TOP
xbs_z = Z_SADDLE_TOP + 15.0

# B2. X-Rails
for sign, side in [(-1,"F"),(1,"R")]:
    box_c(0, sign*X_RAIL_SEP/2, xr_z+HGR20_H/2, X_RAIL_LEN, HGR20_W, HGR20_H,
          L['rail'], "B2 HGR20 X-Rail %s" % side)

# X-Blocks
idx = 1
for sy in [-1, 1]:
    for xx in [-X_RAIL_LEN/4, X_RAIL_LEN/4]:
        box_c(xx, sy*X_RAIL_SEP/2, xr_z+HGR20_H+8,
              HGH20_L, HGH20_W, HGH20_H-HGR20_H,
              L['block'], "B2 HGH20CA X-Block #%d" % idx)
        idx += 1

# F2. X Ball Screw
cyl_x(-X_BS_LEN/2, X_BS_LEN, 0, xbs_z, BS_R, L['screw'], "F2 SFU1605 X-Shaft")
cyl_x(-BS_NUT_L/2, BS_NUT_L, 0, xbs_z, BS_NUT_R, L['screw'], "F2 X-Nut")
cyl_x(-X_BS_LEN/2-BK12_L, BK12_L, 0, xbs_z, BK12_R, L['bearing'], "F2 BK12 X")
cyl_x(X_BS_LEN/2, BF12_L, 0, xbs_z, BF12_R, L['bearing'], "F2 BF12 X")

# A9. T-Slot Table
box_c(0, 0, Z_TABLE_BOT+TABLE_H/2, TABLE_W, TABLE_D, TABLE_H,
      L['table'], "A9 T-Slot Table 550x380x25")

# T-Slot grooves
for i in range(5):
    sy = -TABLE_D/2 + 50 + i*TSLOT_PITCH
    if abs(sy) < TABLE_D/2 - 20:
        box_c(0, sy, Z_TABLE_TOP-TSLOT_D/2, TABLE_W-20, TSLOT_W, TSLOT_D,
              L['tslot'], "A9 T-Slot #%d" % (i+1))

# ================================================================
#  A9 MOUNTING HOLES — T-Slot Table
# ================================================================

# HGH20CA X-Block tapped holes (M6, 4 per block, 4 blocks = 16)
for sy in [-1, 1]:
    for xx_off in [-X_RAIL_LEN/4, X_RAIL_LEN/4]:
        bx = xx_off
        by = sy * X_RAIL_SEP / 2.0
        for ddx in [-25, 25]:
            for ddy in [-16, 16]:
                hole_z(bx+ddx, by+ddy, Z_TABLE_BOT, TABLE_H,
                       HOLE_R_M6, L['hole'], "H M6 X-Block")

# DSG16H X-nut (4× M5 + Ø28 bore)
for dx, dy in [(-24, -18), (24, -18), (-24, 18), (24, 18)]:
    hole_z(dx, dy, Z_TABLE_BOT, TABLE_H,
           HOLE_R_M5, L['hole'], "H M5 DSG16H-X")
hole_z(0, 0, Z_TABLE_BOT, TABLE_H, 14.0, L['hole'], "H Bore DSG16H-X")

# ================================================================
#  Z-AXIS
# ================================================================

zr_y = COL_Y_BACK + WALL_T + 1.0
zr_z_center = BASE_H + COL_HEIGHT/2 + 20

# B3. Z-Rails
for sign, side in [(-1,"L"),(1,"R")]:
    box_c(sign*Z_RAIL_SEP/2, zr_y+HGR20_H/2, zr_z_center,
          HGR20_W, HGR20_H, Z_RAIL_LEN,
          L['rail'], "B3 HGR20 Z-Rail %s" % side)

# Z-Blocks
idx = 1
for sx in [-1, 1]:
    for dz in [-ZCAR_H/4, ZCAR_H/4]:
        box_c(sx*Z_RAIL_SEP/2, zr_y+HGR20_H+8, ZCAR_MID_Z+dz,
              HGH20_W, HGH20_H-HGR20_H, HGH20_L,
              L['block'], "B3 HGH20CA Z-Block #%d" % idx)
        idx += 1

# F3. Z Ball Screw
zbs_y = zr_y + 15
cyl_z(0, zbs_y, zr_z_center-Z_BS_LEN/2, Z_BS_LEN, BS_R,
      L['screw'], "F3 SFU1605 Z-Shaft")
cyl_z(0, zbs_y, ZCAR_MID_Z-BS_NUT_L/2, BS_NUT_L, BS_NUT_R,
      L['screw'], "F3 Z-Nut")
cyl_z(0, zbs_y, zr_z_center+Z_BS_LEN/2, BK12_L, BK12_R,
      L['bearing'], "F3 BK12 Z")
cyl_z(0, zbs_y, zr_z_center-Z_BS_LEN/2-BF12_L, BF12_L, BF12_R,
      L['bearing'], "F3 BF12 Z")

# A10. Z-Carriage
zcar_y = zr_y + HGR20_H + 20 + ZCAR_T/2
box_c(0, zcar_y, ZCAR_MID_Z, ZCAR_W, ZCAR_T, ZCAR_H,
      L['frame'], "A10 Z-Carriage 300x20x260")

# ================================================================
#  A5 MOUNTING HOLES — Column Top Plate (Z-Motor)
# ================================================================

# NEMA23 Z-Motor mount (4× M5 + pilot Ø38.1)
nema_off = 23.57  # 47.14/2
for dx in [-nema_off, nema_off]:
    for dy in [-nema_off, nema_off]:
        hole_z(dx, zbs_y+dy, col_top_z-WALL_T/2, WALL_T,
               HOLE_R_M5, L['hole'], "H M5 NEMA23-Z")
hole_z(0, zbs_y, col_top_z-WALL_T/2, WALL_T,
       19.0, L['hole'], "H Pilot NEMA23-Z")

# ================================================================
#  C. SPINDLE
# ================================================================

sp_y = zcar_y + ZCAR_T/2 + CLAMP_H/2 + 5
sp_z = ZCAR_MID_Z - 20

box_c(0, zcar_y+ZCAR_T/2+8, sp_z, 120, 16, 120,
      L['clamp'], "C1 Spindle Mount Plate")
cyl_z(0, sp_y, sp_z-CLAMP_H/2, CLAMP_H, CLAMP_R,
      L['clamp'], "C2 65mm Clamp")
cyl_z(0, sp_y, sp_z-SPINDLE_LEN/2, SPINDLE_LEN, SPINDLE_R,
      L['spindle'], "C3 Spindle 1.5kW ER16")
cyl_z(0, sp_y, sp_z-SPINDLE_LEN/2-15, 15, ER_R,
      L['spindle'], "C4 ER16 Collet")
cyl_z(0, sp_y, sp_z-SPINDLE_LEN/2-15-ENDMILL_L, ENDMILL_L, ENDMILL_R,
      L['shaft'], "C5 Endmill 8mm")

# ================================================================
#  D. MOTORS
# ================================================================

ym_y = -Y_BS_LEN/2 - BK12_L - COUPLING_L - MOTOR_L/2
box_c(0, ym_y, ybs_z, MOTOR_W, MOTOR_L, MOTOR_W,
      L['motor'], "D1 NEMA23 Y-Motor")
cyl_y(0, -Y_BS_LEN/2-BK12_L-COUPLING_L, COUPLING_L, ybs_z, COUPLING_R,
      L['coupling'], "D1 Y-Coupling")

xm_x = -X_BS_LEN/2 - BK12_L - COUPLING_L - MOTOR_L/2
box_c(xm_x, 0, xbs_z, MOTOR_L, MOTOR_W, MOTOR_W,
      L['motor'], "D2 NEMA23 X-Motor")
cyl_x(-X_BS_LEN/2-BK12_L-COUPLING_L, COUPLING_L, 0, xbs_z, COUPLING_R,
      L['coupling'], "D2 X-Coupling")

zm_z = col_top_z + WALL_T/2 + COUPLING_L + MOTOR_L/2
box_c(0, zbs_y, zm_z, MOTOR_W, MOTOR_W, MOTOR_L,
      L['motor'], "D3 NEMA23 Z-Motor")
cyl_z(0, zbs_y, col_top_z+WALL_T/2, COUPLING_L, COUPLING_R,
      L['coupling'], "D3 Z-Coupling")

# ================================================================
#  E. 4TH AXIS ROTARY
# ================================================================

rot_x = 100.0
rot_z = Z_TABLE_TOP

box_c(rot_x, 0, rot_z+ROTARY_BASE_H/2, ROTARY_BASE, ROTARY_BASE, ROTARY_BASE_H,
      L['rotary'], "E1 Rotary Base")
cyl_x(rot_x-CHUCK_L/2, CHUCK_L, 0, rot_z+ROTARY_BASE_H+CHUCK_R, CHUCK_R,
      L['rotary'], "E2 K11-80 Chuck")

ts_x = -120.0
chuck_z = rot_z + ROTARY_BASE_H + CHUCK_R
box_c(ts_x, 0, rot_z+TAILSTOCK_H/2, TAILSTOCK_W, TAILSTOCK_W, TAILSTOCK_H,
      L['rotary'], "E3 Tailstock MT2")
cyl_x(ts_x+TAILSTOCK_W/2, rot_x-CHUCK_L/2-ts_x-TAILSTOCK_W/2, 0, chuck_z, 3.0,
      L['shaft'], "E3 Center")

box_c(rot_x+CHUCK_L/2+COUPLING_L+MOTOR_L/2, 0, chuck_z,
      MOTOR_L, MOTOR_W*0.85, MOTOR_W*0.85,
      L['motor'], "D4 NEMA23 A-Motor")

# ================================================================
#  WORK VOLUME — 엣지 라인만 (투명)
# ================================================================

wv_z = Z_TABLE_TOP + WA_Z/2 + 5
pts = [
    (-WA_X/2,-WA_Y/2,wv_z-WA_Z/2),( WA_X/2,-WA_Y/2,wv_z-WA_Z/2),
    ( WA_X/2, WA_Y/2,wv_z-WA_Z/2),(-WA_X/2, WA_Y/2,wv_z-WA_Z/2),
    (-WA_X/2,-WA_Y/2,wv_z+WA_Z/2),( WA_X/2,-WA_Y/2,wv_z+WA_Z/2),
    ( WA_X/2, WA_Y/2,wv_z+WA_Z/2),(-WA_X/2, WA_Y/2,wv_z+WA_Z/2),
]
for a, b in [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]:
    lid = rs.AddLine(pts[a], pts[b])
    if lid:
        rs.ObjectLayer(lid, L['workvol'])

# ================================================================
#  LABELS
# ================================================================

rs.AddTextDot("CNC-FC350 | 350x300x150mm", (0, 0, -30))
rs.AddTextDot("Work Volume 350x300x150", (0, 0, wv_z+WA_Z/2+10))

# ================================================================
#  FINISH
# ================================================================

rs.EnableRedraw(True)
rs.ZoomExtents()

try:
    rs.ViewDisplayMode(rs.CurrentView(), "Shaded")
except:
    pass

print("=" * 50)
print("  CNC-FC350 Phase 2 — Generated OK!")
print("  Table top: Z = %.0f mm" % Z_TABLE_TOP)
print("  Parts: ~70 body + ~120 mounting holes")
print("  Layers: 18 (frame/linear/screw/motor/holes)")
print("  Hole layers: G_MountHoles (red), G_DowelPins (orange)")
print("  Toggle holes: Layer panel > G_MountHoles on/off")
print("=" * 50)
