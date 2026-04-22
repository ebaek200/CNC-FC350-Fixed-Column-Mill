# -*- coding: utf-8 -*-
# CNC-FC350 Fixed-Column Box-Frame Mill — Fusion 360
# 350x300x150mm | HGR20 + SFU1605 | 6061-T6 Box Column
import adsk.core, adsk.fusion, traceback

def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.DirectDesignType
        root = design.rootComponent

        # All dimensions in cm (Fusion internal unit)
        # 700mm = 70cm, 25mm = 2.5cm, etc.

        # --- helpers ---
        NB = adsk.fusion.FeatureOperations.NewBodyFeatureOperation

        def _offset_plane(comp, base_plane, offset_cm):
            """Create offset construction plane."""
            inp = comp.constructionPlanes.createInput()
            inp.setByOffset(base_plane, adsk.core.ValueInput.createByReal(offset_cm))
            return comp.constructionPlanes.add(inp)

        def box(name, cx, cy, cz, sx, sy, sz):
            """Box centered at (cx,cy,cz), size (sx,sy,sz) in cm."""
            occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            c = occ.component; c.name = name
            zbot = cz - sz / 2.0
            plane = _offset_plane(c, c.xYConstructionPlane, zbot)
            sk = c.sketches.add(plane)
            sk.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(cx - sx/2, cy - sy/2, 0),
                adsk.core.Point3D.create(cx + sx/2, cy + sy/2, 0))
            c.features.extrudeFeatures.addSimple(
                sk.profiles.item(0),
                adsk.core.ValueInput.createByReal(sz), NB)
            return c

        def cylZ(name, cx, cy, zbot, h, r):
            """Cylinder along Z, base at zbot."""
            occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            c = occ.component; c.name = name
            plane = _offset_plane(c, c.xYConstructionPlane, zbot)
            sk = c.sketches.add(plane)
            sk.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(cx, cy, 0), r)
            c.features.extrudeFeatures.addSimple(
                sk.profiles.item(0),
                adsk.core.ValueInput.createByReal(h), NB)
            return c

        def cylY(name, cx, ystart, length, cz, r):
            """Cylinder along Y, start at ystart."""
            occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            c = occ.component; c.name = name
            plane = _offset_plane(c, c.xZConstructionPlane, ystart)
            sk = c.sketches.add(plane)
            sk.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(cx, cz, 0), r)
            c.features.extrudeFeatures.addSimple(
                sk.profiles.item(0),
                adsk.core.ValueInput.createByReal(length), NB)
            return c

        def cylX(name, xstart, length, cy, cz, r):
            """Cylinder along X, start at xstart."""
            occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            c = occ.component; c.name = name
            plane = _offset_plane(c, c.yZConstructionPlane, xstart)
            sk = c.sketches.add(plane)
            sk.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(cy, cz, 0), r)
            c.features.extrudeFeatures.addSimple(
                sk.profiles.item(0),
                adsk.core.ValueInput.createByReal(length), NB)
            return c

        # ========== DIMENSIONS (cm) ==========
        BW, BD, BH = 70.0, 60.0, 2.5          # Base plate
        CW, CD, CH, WT = 45.0, 22.0, 52.0, 2.5  # Column
        SW, SD, SH = 48.0, 40.0, 2.0          # Saddle
        TW, TD, TH = 55.0, 38.0, 2.5          # Table
        ZW, ZH, ZT = 30.0, 26.0, 2.0          # Z-carriage

        HR_W, HR_H = 2.0, 2.75                # HGR20
        BK_W, BK_L = 4.4, 7.75                # HGH20CA

        YRL, YRS = 50.0, 24.0                 # Y-rail len, sep
        XRL, XRS = 55.0, 28.0                 # X-rail
        ZRL, ZRS = 36.0, 22.0                 # Z-rail

        BSR, NR, NL = 0.8, 1.4, 4.0           # Ball screw
        BKR, BKL = 1.9, 2.1                   # BK12
        BFR, BFL = 1.5, 1.5                   # BF12
        YBL, XBL, ZBL = 46.0, 51.0, 32.0      # BS lengths

        SPR, SPL = 3.25, 20.0                 # Spindle
        CLR, CLH = 4.5, 5.5                   # Clamp
        MW, ML = 5.7, 5.6                     # Motor
        CPR, CPL = 1.25, 2.5                  # Coupling

        # Z stack-up
        ZBT = BH                               # 2.5
        ZSB = ZBT + HR_H + 1.6                # 6.85
        ZST = ZSB + SH                        # 8.85
        ZTB = ZST + HR_H + 1.6                # 13.2
        ZTT = ZTB + TH                        # 15.7

        # Column positions
        CYB = -BD / 2.0                        # -30
        CYC = CYB + CD / 2.0                   # -19
        BWY = CYB + WT / 2.0                   # -28.75
        LWX = -(CW/2 - WT/2)                   # -21.25
        RWX = CW/2 - WT/2                      # 21.25
        CCZ = BH + CH / 2.0                    # 28.5
        CTZ = BH + CH + WT / 2.0               # 55.75

        # Z-axis
        ZRY = CYB + WT + 0.1                   # -27.4
        ZRZC = BH + CH/2 + 2.0                 # 30.5
        ZBSY = ZRY + 1.5                       # -25.9
        ZCMZ = ZTT + 10.0 + ZH/2              # 38.7
        ZCRY = ZRY + HR_H + 2.0 + ZT/2        # -22.65

        YBSZ = ZBT + 1.5                       # 4.0
        XBSZ = ZST + 1.5                       # 10.35

        # ========== A. FRAME ==========
        box("A1 Base Plate 700x600x25", 0, 0, BH/2, BW, BD, BH)
        box("A2 Column Back Wall", 0, BWY, CCZ, CW, WT, CH)
        box("A3 Column Left Wall", LWX, CYC, CCZ, WT, CD, CH)
        box("A4 Column Right Wall", RWX, CYC, CCZ, WT, CD, CH)
        box("A5 Column Top Plate", 0, CYC, CTZ, CW, CD, WT)

        for i, (gx, gy) in enumerate([
            (LWX, CYB+WT), (RWX, CYB+WT),
            (LWX, CYB+CD-WT), (RWX, CYB+CD-WT)]):
            box("A6 Gusset #%d" % (i+1), gx, gy, BH+3, 2, 2, 6)

        for i, (fx, fy) in enumerate([(31,-26),(-31,-26),(31,26),(-31,26)]):
            cylZ("A7 Foot #%d" % (i+1), fx, fy, -1.5, 1.5, 2.0)

        box("A8 Y-Saddle 480x400x20", 0, 0, ZSB+SH/2, SW, SD, SH)
        box("A9 T-Slot Table 550x380x25", 0, 0, ZTB+TH/2, TW, TD, TH)
        box("A10 Z-Carriage 300x20x260", 0, ZCRY, ZCMZ, ZW, ZT, ZH)

        # T-slots
        for i in range(5):
            sy = -14 + i * 6
            box("T-Slot #%d" % (i+1), 0, sy, ZTT-0.6, TW-2, 0.85, 1.2)

        # ========== B. RAILS ==========
        for s, n in [(-1,"L"),(1,"R")]:
            box("B1 Y-Rail %s"%n, s*YRS/2, 0, ZBT+HR_H/2, HR_W, YRL, HR_H)
        for s in [-1,1]:
            for yy in [-YRL/4, YRL/4]:
                box("B1 Y-Blk", s*YRS/2, yy, ZBT+HR_H+0.8, BK_W, BK_L, 1.6)

        for s, n in [(-1,"F"),(1,"R")]:
            box("B2 X-Rail %s"%n, 0, s*XRS/2, ZST+HR_H/2, XRL, HR_W, HR_H)
        for s in [-1,1]:
            for xx in [-XRL/4, XRL/4]:
                box("B2 X-Blk", xx, s*XRS/2, ZST+HR_H+0.8, BK_L, BK_W, 1.6)

        for s, n in [(-1,"L"),(1,"R")]:
            box("B3 Z-Rail %s"%n, s*ZRS/2, ZRY+HR_H/2, ZRZC, HR_W, HR_H, ZRL)
        for s in [-1,1]:
            for dz in [-ZH/4, ZH/4]:
                box("B3 Z-Blk", s*ZRS/2, ZRY+HR_H+0.8, ZCMZ+dz, BK_W, 1.6, BK_L)

        # ========== F. BALL SCREWS ==========
        cylY("F1 Y-Shaft", 0, -YBL/2, YBL, YBSZ, BSR)
        cylY("F1 Y-Nut", 0, -NL/2, NL, YBSZ, NR)
        cylY("F1 BK12 Y", 0, -YBL/2-BKL, BKL, YBSZ, BKR)
        cylY("F1 BF12 Y", 0, YBL/2, BFL, YBSZ, BFR)

        cylX("F2 X-Shaft", -XBL/2, XBL, 0, XBSZ, BSR)
        cylX("F2 X-Nut", -NL/2, NL, 0, XBSZ, NR)
        cylX("F2 BK12 X", -XBL/2-BKL, BKL, 0, XBSZ, BKR)
        cylX("F2 BF12 X", XBL/2, BFL, 0, XBSZ, BFR)

        cylZ("F3 Z-Shaft", 0, ZBSY, ZRZC-ZBL/2, ZBL, BSR)
        cylZ("F3 Z-Nut", 0, ZBSY, ZCMZ-NL/2, NL, NR)
        cylZ("F3 BK12 Z", 0, ZBSY, ZRZC+ZBL/2, BKL, BKR)
        cylZ("F3 BF12 Z", 0, ZBSY, ZRZC-ZBL/2-BFL, BFL, BFR)

        # ========== C. SPINDLE ==========
        spy = ZCRY + ZT/2 + CLH/2 + 0.5
        spz = ZCMZ - 2.0
        box("C1 Mount Plate", 0, ZCRY+ZT/2+0.8, spz, 12, 1.6, 12)
        cylZ("C2 65mm Clamp", 0, spy, spz-CLH/2, CLH, CLR)
        cylZ("C3 Spindle 1.5kW", 0, spy, spz-SPL/2, SPL, SPR)
        cylZ("C4 ER16", 0, spy, spz-SPL/2-1.5, 1.5, 1.2)
        cylZ("C5 Endmill", 0, spy, spz-SPL/2-6.5, 5, 0.4)

        # ========== D. MOTORS ==========
        ymy = -YBL/2 - BKL - CPL - ML/2
        box("D1 Y-Motor", 0, ymy, YBSZ, MW, ML, MW)
        cylY("D1 Y-Coup", 0, -YBL/2-BKL-CPL, CPL, YBSZ, CPR)

        xmx = -XBL/2 - BKL - CPL - ML/2
        box("D2 X-Motor", xmx, 0, XBSZ, ML, MW, MW)
        cylX("D2 X-Coup", -XBL/2-BKL-CPL, CPL, 0, XBSZ, CPR)

        zmz = CTZ + WT/2 + CPL + ML/2
        box("D3 Z-Motor", 0, ZBSY, zmz, MW, MW, ML)
        cylZ("D3 Z-Coup", 0, ZBSY, CTZ+WT/2, CPL, CPR)

        # ========== E. ROTARY ==========
        rx = 10.0
        box("E1 Rotary Base", rx, 0, ZTT+1.5, 10, 10, 3)
        cylX("E2 K11-80 Chuck", rx-2, 4, 0, ZTT+3+4, 4)
        box("E3 Tailstock", -12, 0, ZTT+2.5, 6, 6, 5)
        box("D4 A-Motor", rx+2+CPL+ML/2, 0, ZTT+3+4, ML, MW*0.85, MW*0.85)

        # ========== REF ==========
        box("REF WorkVol 350x300x150", 0, 0, ZTT+8, 35, 30, 15)

        app.activeViewport.fit()
        ui.messageBox(
            'CNC-FC350 OK!\n'
            'Table top: Z=%.1fcm (%.0fmm)\n'
            '~65 components' % (ZTT, ZTT*10))

    except:
        if ui:
            ui.messageBox('Error:\n{}'.format(traceback.format_exc()))
