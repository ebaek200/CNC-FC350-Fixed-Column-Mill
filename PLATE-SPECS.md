# CNC-FC350 — Frame Plate Specifications (Phase 2)
# 프레임 플레이트 상세 가공 사양서
# Material: 6061-T6 Aluminum, Anodized (Black or Natural)
# Tolerance: ±0.02mm (critical), ±0.05mm (general)
# Surface Finish: Ra 1.6 (machined surfaces), Ra 3.2 (non-critical)

## Coordinate System
- Origin: Center of Base Plate bottom surface
- X: Left(-) / Right(+)  (operator facing front)
- Y: Rear(-) / Front(+)
- Z: Down(-) / Up(+)

## Z Stack-Up Reference
| Level | Z (mm) | Description |
|-------|--------|-------------|
| Base bottom | 0 | Origin |
| Base top | 25 | HGR20 Y-rail mount surface |
| Y-rail top | 52.5 | = 25 + 27.5 |
| Y-block top | 68.5 | = 52.5 + 16 |
| Saddle bottom | 68.5 | = Y-block top |
| Saddle top | 88.5 | = 68.5 + 20 |
| X-rail top | 116.0 | = 88.5 + 27.5 |
| X-block top | 132.0 | = 116 + 16 |
| Table bottom | 132.0 | = X-block top |
| Table top | 157.0 | = 132 + 25 |

## Column Y Reference
| Position | Y (mm) | Description |
|----------|--------|-------------|
| Column back face | -300 | = -BASE_D/2 |
| Back wall center | -287.5 | = -300 + 12.5 |
| Column front face | -80 | = -300 + 220 |
| Column center | -190 | = -300 + 110 |

---

## A1. Base Plate — 700 × 600 × 25mm

### Overview
- **Size**: 700(X) × 600(Y) × 25(Z) mm
- **Material**: 6061-T6, 25mm thick
- **Weight**: ~28 kg
- **Function**: Foundation plate. Mounts Y-axis rails, ball screw supports, column walls, leveling feet.

### Top Surface Holes (Z = 25mm)

#### HGR20 Y-Rail Mounting (2 rails, 16 holes)
- Rail X positions: X = ±120mm (Y_RAIL_SEP/2 = 240/2)
- Rail runs Y = -250 to +250 (500mm centered)
- Hole pitch: 60mm along Y
- Starting 30mm from rail ends → Y = -220, -160, -100, -40, +20, +80, +140, +200
- **Hole type**: M5 counterbore (Ø9 × 5.5mm deep + M5 × 19.5mm through)
- **Total**: 8 holes/rail × 2 rails = **16 holes**

| Rail | X | Y positions (8 per rail) |
|------|---|--------------------------|
| Left | -120 | -220, -160, -100, -40, +20, +80, +140, +200 |
| Right | +120 | -220, -160, -100, -40, +20, +80, +140, +200 |

#### BK12 Y-Axis Fixed End (2 holes)
- BK12 center: (0, -230, 25)
- Hole spacing: 32mm in X direction
- **Positions**: (-16, -230), (+16, -230)
- **Hole type**: M5 through + counterbore, Ø13 recess for BK12 pilot

#### BF12 Y-Axis Free End (2 holes)
- BF12 center: (0, +230, 25)
- Hole spacing: 32mm in X direction
- **Positions**: (-16, +230), (+16, +230)
- **Hole type**: M5 through + counterbore

#### Column Back Wall (A2) Mounting (6 holes + 2 dowels)
- Wall Y center: Y = -287.5
- M10 bolt positions along X: -200, -120, -40, +40, +120, +200
- **Positions**: (X, -287.5) for each X value above
- **Hole type**: M10 clearance (Ø11) through, counterbore Ø18 × 8mm from bottom
- **Dowel pins**: Ø8H7 at (-100, -287.5) and (+100, -287.5)

#### Column Left Wall (A3) Mounting (4 holes + 2 dowels)
- Wall X center: X = -212.5
- M10 bolt positions along Y: -270, -230, -150, -110
- **Positions**: (-212.5, Y) for each Y value above
- **Hole type**: M10 clearance (Ø11) through, counterbore Ø18 × 8mm from bottom
- **Dowel pins**: Ø8H7 at (-212.5, -250) and (-212.5, -130)

#### Column Right Wall (A4) Mounting (4 holes + 2 dowels)
- Same as A3 but at X = +212.5
- **Positions**: (+212.5, Y) for Y = -270, -230, -150, -110
- **Dowel pins**: Ø8H7 at (+212.5, -250) and (+212.5, -130)

### Bottom Surface Holes (Z = 0mm)

#### Leveling Feet (4 holes)
- **Positions**: (±310, ±260)
- **Hole type**: M12 × 15mm tapped (blind, from bottom)

### Summary A1
| Feature | Count | Hole Type |
|---------|-------|-----------|
| HGR20 Y-rail mounting | 16 | M5 CB |
| BK12 mounting | 2 + 1 pilot | M5 CB |
| BF12 mounting | 2 | M5 CB |
| Column back wall | 6 + 2 dowel | M10 CL + Ø8H7 |
| Column left wall | 4 + 2 dowel | M10 CL + Ø8H7 |
| Column right wall | 4 + 2 dowel | M10 CL + Ø8H7 |
| Leveling feet | 4 | M12 tapped |
| **Total** | **~44 holes** | |

---

## A2. Column Back Wall — 450 × 520 × 25mm

### Overview
- **Size**: 450(X) × 520(Z) × 25(Y) mm
- **Material**: 6061-T6, 25mm thick
- **Weight**: ~16 kg
- **Function**: Rear wall of column. Mounts Z-axis rails and ball screw bearing.

### Front Face Holes (facing operator, Y = -275)

#### HGR20 Z-Rail Mounting (2 rails, ~10 holes)
- Rail X positions: X = ±110mm (Z_RAIL_SEP/2 = 220/2)
- Rail runs Z = 105 to 465 (360mm, centered at Z=285)
- Hole pitch: 60mm along Z
- **Positions**: Z = 125, 185, 245, 305, 365, 425 (6 per rail)
- **Hole type**: M5 counterbore
- **Total**: 6 × 2 = **12 holes**

#### BK12 Z-Axis Fixed End (2 holes, top)
- Center: (0, wall_y, top of rail range)
- **Positions**: (±16, -275, 445)
- **Hole type**: M5 counterbore

#### BF12 Z-Axis Free End (2 holes, bottom)
- **Positions**: (±16, -275, 125)
- **Hole type**: M5 counterbore

### Rear Face (Y = -300)

#### Connection to Base Plate A1 (from below)
- Receives M10 bolts from A1 base → M10 tapped holes in bottom edge
- **6 positions**: X = -200, -120, -40, +40, +120, +200 at Z = 25 (bottom edge)
- **Hole type**: M10 × 20mm tapped (blind)
- **Dowel**: Ø8H7 at X = ±100

#### Connection to Side Walls A3/A4
- M8 bolts connecting side walls to back wall edges
- Left edge: X = -212.5, Z = 85, 185, 285, 385, 485 → **5 holes M8 tapped**
- Right edge: X = +212.5, same Z values → **5 holes M8 tapped**

### Summary A2
| Feature | Count | Hole Type |
|---------|-------|-----------|
| HGR20 Z-rail mounting | 12 | M5 CB |
| BK12 Z fixed | 2 | M5 CB |
| BF12 Z free | 2 | M5 CB |
| Base plate connection | 6 + 2 dowel | M10 tapped + Ø8H7 |
| Side wall connection | 10 | M8 tapped |
| **Total** | **~34 holes** | |

---

## A3/A4. Column Side Walls — 25 × 220 × 520mm (×2, mirrored)

### Overview
- **Size**: 25(X) × 220(Y) × 520(Z) mm
- **Material**: 6061-T6, 25mm thick
- **Weight**: ~7.5 kg each
- **Function**: Side walls of column box frame. Provides lateral rigidity.

### Outer Face Holes

#### Connection to Back Wall A2 (rear edge)
- Y = -287.5 (rear edge of side wall)
- M8 clearance holes at Z = 85, 185, 285, 385, 485
- **5 holes M8 clearance (Ø9)** per wall

#### Connection to Base Plate A1 (bottom edge)
- Z = 25 (bottom of wall, sitting on base)
- Receives M10 bolts from below → M10 tapped in bottom face
- **4 positions along Y**: Y = -270, -230, -150, -110
- **Hole type**: M10 × 20mm tapped (blind, from bottom face)
- **Dowels**: Ø8H7 at Y = -250, -130

#### Connection to Top Plate A5 (top edge)
- Z = 545 (top of wall)
- M8 bolt positions along Y: -270, -210, -150, -110
- **4 holes M8 tapped** per wall (from top face)

#### Gusset Mounting (4 per wall)
- Bottom gussets at Z ≈ 55 (BASE_H + GUSSET_S/2)
- Top gussets at Z ≈ 485 (BASE_H + COL_HEIGHT - GUSSET_S/2)
- Y = -275 (near back) and Y = -105 (near front)
- **2 × M6 per gusset** → 8 holes M6 per wall

### Summary A3/A4 (each)
| Feature | Count | Hole Type |
|---------|-------|-----------|
| Back wall connection | 5 | M8 clearance |
| Base plate connection | 4 + 2 dowel | M10 tapped + Ø8H7 |
| Top plate connection | 4 | M8 tapped |
| Gusset mounting | 8 | M6 tapped |
| **Total per wall** | **~23 holes** | |

---

## A5. Column Top Plate — 450 × 220 × 25mm

### Overview
- **Size**: 450(X) × 220(Y) × 25(Z) mm
- **Material**: 6061-T6, 25mm thick
- **Weight**: ~6.5 kg
- **Function**: Top cap of column. Rigidity + Z-motor mount.

### Bottom Face Holes

#### Connection to Side Walls A3/A4
- M8 clearance holes into side wall tops
- Left (X = -212.5): Y = -270, -210, -150, -110 → **4 holes**
- Right (X = +212.5): same → **4 holes**
- **Hole type**: M8 clearance (Ø9) through

### Top Face Holes

#### Z-Axis Motor (NEMA23) Mount
- Motor center: (0, zbs_y ≈ -259)
- NEMA23 pattern: 47.14mm diagonal → holes at ±23.57mm in X and Y
- **4 holes M5** at (±23.57, -259 ± 23.57)
- **Pilot bore**: Ø38.1mm through (for motor shaft/coupling)

#### Z Ball Screw Through Hole
- Center: (0, -259)
- **Ø20mm through** for ball screw shaft passage

### Summary A5
| Feature | Count | Hole Type |
|---------|-------|-----------|
| Side wall connection | 8 | M8 clearance |
| NEMA23 Z-motor mount | 4 + 1 pilot | M5 + Ø38.1 |
| Ball screw passage | 1 | Ø20 through |
| **Total** | **~14 holes** | |

---

## A8. Y-Saddle Plate — 480 × 400 × 20mm

### Overview
- **Size**: 480(X) × 400(Y) × 20(Z) mm
- **Material**: 6061-T6, 20mm thick
- **Weight**: ~14 kg
- **Function**: Y-axis moving plate. Connects Y-blocks (bottom) to X-rails (top).

### Bottom Face (Z = 68.5)

#### HGH20CA Y-Block Mounting (4 blocks, 16 holes)
- Block pattern: 32mm(X) × 50mm(Y), M6 tapped
- Block positions:
  - L-Front: (-120, +125) → holes at (-136,-152,-104,-98, etc.)
  - L-Rear: (-120, -125)
  - R-Front: (+120, +125)
  - R-Rear: (+120, -125)
- **4 holes M6 per block** × 4 blocks = **16 holes M6 tapped**

#### Y Ball Screw Nut (DSG16H) Mounting
- Nut center: (0, 0, 68.5)
- DSG16H pattern: ~48mm(X) × 36mm(Y), 4× M5
- **4 holes M5 tapped**
- **Ø28mm bore** through for ball screw nut clearance

### Top Face (Z = 88.5)

#### HGR20 X-Rail Mounting (2 rails, ~16 holes)
- Rail Y positions: Y = ±140mm (X_RAIL_SEP/2 = 280/2)
- Rail length: 550mm → exceeds saddle (480mm), so only holes within saddle range
- Hole pitch: 60mm along X
- X positions: -210, -150, -90, -30, +30, +90, +150, +210 (8 per rail, within ±240)
- **Hole type**: M5 counterbore
- **Total**: 8 × 2 = **16 holes**

#### X Ball Screw BK12 Mount (2 holes, left side)
- **Positions**: (±16, 0) relative to BK12 center at X = -255
- → (-271, 0) and (-239, 0)
- **Hole type**: M5 counterbore

#### X Ball Screw BF12 Mount (2 holes, right side)
- **Positions**: relative to BF12 center at X = +255
- → (+239, 0) and (+271, 0)
- **Hole type**: M5 counterbore

### Summary A8
| Feature | Count | Hole Type |
|---------|-------|-----------|
| HGH20CA Y-block (bottom) | 16 | M6 tapped |
| DSG16H Y-nut (bottom) | 4 + 1 bore | M5 + Ø28 |
| HGR20 X-rail (top) | 16 | M5 CB |
| BK12 X fixed | 2 | M5 CB |
| BF12 X free | 2 | M5 CB |
| **Total** | **~41 holes** | |

---

## A9. T-Slot Table — 550 × 380 × 25mm

### Overview
- **Size**: 550(X) × 380(Y) × 25(Z) mm
- **Material**: 6061-T6, 25mm thick
- **Weight**: ~14 kg
- **Function**: Workholding surface. T-slots for clamps, vise, rotary.

### Bottom Face (Z = 132)

#### HGH20CA X-Block Mounting (4 blocks, 16 holes)
- Block pattern: 50mm(X) × 32mm(Y), M6 tapped
- Block positions:
  - F-Left: (-137.5, -140)
  - F-Right: (+137.5, -140)
  - R-Left: (-137.5, +140)
  - R-Right: (+137.5, +140)
- **4 holes M6 per block** × 4 = **16 holes M6 tapped**

#### X Ball Screw Nut (DSG16H) Mounting
- Nut center: (0, 0)
- **4 holes M5 tapped**
- **Ø28mm bore** through for nut clearance

### Top Face (Z = 157)

#### T-Slots (5 slots)
- Slot profile: 8.5mm wide opening, 12mm deep, T-shape (14mm at bottom)
- Y positions: -120, -60, 0, +60, +120 (pitch 60mm)
- Length: 530mm (TABLE_W - 20)
- Running in X direction

### Summary A9
| Feature | Count | Hole Type |
|---------|-------|-----------|
| HGH20CA X-block (bottom) | 16 | M6 tapped |
| DSG16H X-nut (bottom) | 4 + 1 bore | M5 + Ø28 |
| T-slots (top) | 5 | CNC milled |
| **Total** | **~21 holes + 5 slots** | |

---

## A10. Z-Carriage Plate — 300 × 260 × 20mm

### Overview
- **Size**: 300(X) × 260(Z) × 20(Y) mm
- **Material**: 6061-T6, 20mm thick
- **Weight**: ~4.2 kg
- **Function**: Z-axis moving plate. Connects Z-blocks (rear) to spindle mount (front).

### Rear Face (facing column)

#### HGH20CA Z-Block Mounting (4 blocks, 16 holes)
- Block pattern: 32mm(X) × 50mm(Z), M6 tapped
- Block positions on carriage:
  - L-Top: (-110, mid_z + 65)
  - L-Bottom: (-110, mid_z - 65)
  - R-Top: (+110, mid_z + 65)
  - R-Bottom: (+110, mid_z - 65)
- **4 holes M6 per block** × 4 = **16 holes M6 tapped**

#### Z Ball Screw Nut (DSG16H) Mounting
- Nut center: (0, mid_z)
- **4 holes M5 tapped**
- **Ø28mm bore** through for nut clearance

### Front Face (facing operator)

#### Spindle Mount Plate Holes
- 120 × 120mm mount plate pattern
- **4 holes M8** at corners (±50, mid_z ± 50)
- **Central bore**: Ø70mm for spindle body passage

### Summary A10
| Feature | Count | Hole Type |
|---------|-------|-----------|
| HGH20CA Z-block (rear) | 16 | M6 tapped |
| DSG16H Z-nut (rear) | 4 + 1 bore | M5 + Ø28 |
| Spindle mount (front) | 4 + 1 bore | M8 + Ø70 |
| **Total** | **~25 holes** | |

---

## A6. Gusset Reinforcements — 60 × 20 × 60mm (×8)

### Overview
- **Size**: 60(Z) × 20 × 20mm (right-triangle profile preferred)
- **Material**: 6061-T6
- **Function**: Corner reinforcement between column walls and base/top
- **Mounting**: 2× M6 per gusset into side wall

---

## Bill of Machining Summary

| Plate | Qty | Size (mm) | Thickness | Total Holes | Critical Features |
|-------|-----|-----------|-----------|-------------|-------------------|
| A1 Base | 1 | 700×600 | 25 | ~44 | Rail grooves, dowel holes |
| A2 Back Wall | 1 | 450×520 | 25 | ~34 | Z-rail mounting face |
| A3 Left Wall | 1 | 25×220×520 | 25 | ~23 | — |
| A4 Right Wall | 1 | 25×220×520 | 25 | ~23 | Mirror of A3 |
| A5 Top Plate | 1 | 450×220 | 25 | ~14 | Motor mount, through hole |
| A6 Gussets | 8 | 60×20×60 | 20 | ~2 each | Simple |
| A7 Leveling Feet | 4 | Ø40×15 | — | — | M12 thread |
| A8 Y-Saddle | 1 | 480×400 | 20 | ~41 | Both-side features |
| A9 T-Slot Table | 1 | 550×380 | 25 | ~21+5 slots | T-slot milling |
| A10 Z-Carriage | 1 | 300×260 | 20 | ~25 | Both-side features |
| **Total** | **~20 parts** | | | **~260 holes** | |

---

## Tolerances

| Feature | Tolerance | Note |
|---------|-----------|------|
| Rail mounting surfaces | ±0.02mm flatness | Critical for accuracy |
| Dowel pin holes | Ø8H7 (+0/+0.015) | Alignment critical |
| Rail bolt holes | M5 ±0.05mm position | Standard |
| Block tapped holes | M6 ±0.05mm position | Standard |
| T-slot dimensions | ±0.05mm | Standard |
| Plate thickness | ±0.05mm | General |
| Overall dimensions | ±0.1mm | General |
| Surface parallelism | 0.02mm/100mm | Rail surfaces |

---

## Surface Treatment
- **All plates**: Bead blast + Hard anodize (Type III) or Natural anodize (Type II)
- **Rail mounting surfaces**: Leave raw (masked during anodize) for maximum flatness
- **Threaded holes**: Tap after anodize

## Notes for Factory
1. All dimensions in millimeters
2. Material: 6061-T6 (not 6063, not cast)
3. Deburr all edges
4. Mark part number on non-critical surface
5. Pack each part individually
6. Include material certificate (mill cert)
