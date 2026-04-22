# -*- coding: utf-8 -*-
# ================================================================
# STEP Assembly BOM Extractor — Rhino 8 Mac
# Usage: Open STEP file in Rhino first, then run this script
# Auto-explodes blocks/groups to get individual parts
# ================================================================

import rhinoscriptsyntax as rs

# Step 1: Get all objects
all_objs = rs.AllObjects()
if not all_objs:
    print("No objects found. Open a STEP file first!")
else:
    print("Initial objects: %d" % len(all_objs))
    print("Exploding blocks/groups...")

    # Step 2: Recursively explode everything (blocks, groups, polysurfaces)
    max_rounds = 5
    for rnd in range(max_rounds):
        to_explode = []
        current = rs.AllObjects()
        for oid in current:
            otype = rs.ObjectType(oid)
            # 4096 = Block Instance, 16 = Polysurface (joined brep)
            if otype == 4096:
                to_explode.append(oid)

        if not to_explode:
            break

        print("  Round %d: exploding %d blocks..." % (rnd + 1, len(to_explode)))
        for oid in to_explode:
            try:
                rs.ExplodeBlockInstance(oid)
            except:
                try:
                    rs.ExplodeObjects(oid, True)
                except:
                    pass

    # Step 3: Final object list
    all_objs = rs.AllObjects()
    print("After explode: %d objects" % len(all_objs))

    # Step 4: Collect part info
    parts = {}
    unnamed_count = 0
    for oid in all_objs:
        name = rs.ObjectName(oid)
        layer = rs.ObjectLayer(oid) or ""

        # Use layer name if object has no name
        if not name or name.strip() == "":
            # Try parent layer for hierarchy
            if "::" in layer:
                name = layer.split("::")[-1]
            elif layer:
                name = layer
            else:
                unnamed_count += 1
                name = "(unnamed_%d)" % unnamed_count

        otype = rs.ObjectType(oid)
        type_names = {
            1: "Point", 4: "Curve", 8: "Surface", 16: "Polysrf",
            32: "Mesh", 256: "Light", 512: "Annot",
            4096: "Block", 8192: "Text", 65536: "Extrusion"
        }
        tname = type_names.get(otype, "T%d" % otype)

        key = name.strip()
        if key in parts:
            parts[key]['count'] += 1
        else:
            bbox = rs.BoundingBox(oid)
            size_str = ""
            if bbox and len(bbox) >= 5:
                dx = abs(bbox[1][0] - bbox[0][0])
                dy = abs(bbox[3][1] - bbox[0][1])
                dz = abs(bbox[4][2] - bbox[0][2])
                size_str = "%.1f x %.1f x %.1f" % (dx, dy, dz)

            parts[key] = {
                'count': 1,
                'layer': layer,
                'type': tname,
                'size': size_str
            }

    # Step 5: Sort by count (descending), then name
    sorted_parts = sorted(parts.items(), key=lambda x: (-x[1]['count'], x[0]))

    # Print BOM
    print("")
    print("=" * 80)
    print("  BOM — %d unique parts, %d total objects" % (len(parts), len(all_objs)))
    print("=" * 80)
    print("%-4s %-40s %4s %-8s %s" % ("#", "Part Name", "Qty", "Type", "Size (mm)"))
    print("-" * 80)

    for i, (name, info) in enumerate(sorted_parts, 1):
        print("%-4d %-40s %4d %-8s %s" % (
            i,
            name[:40],
            info['count'],
            info['type'],
            info['size']
        ))

    print("-" * 80)
    print("Total: %d unique parts, %d objects" % (len(parts), len(all_objs)))

    # Layer hierarchy (STEP assemblies often use nested layers)
    print("")
    print("=" * 80)
    print("  Layer Hierarchy")
    print("=" * 80)
    layers = {}
    for oid in all_objs:
        ly = rs.ObjectLayer(oid) or "(default)"
        if ly in layers:
            layers[ly] += 1
        else:
            layers[ly] = 1

    for ly, cnt in sorted(layers.items()):
        depth = ly.count("::")
        indent = "  " * depth
        short = ly.split("::")[-1] if "::" in ly else ly
        print("  %s%-40s  %d objects" % (indent, short[:40], cnt))
