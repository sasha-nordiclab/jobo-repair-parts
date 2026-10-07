#!/usr/bin/env python3
"""Turn a FreeCAD .FCStd archive into readable text for `git diff`.

Prints each object with its label, type, links, numeric parameters,
expressions and dimensional sketch constraints. Geometry (.brp) is skipped.
"""
import math
import sys
import xml.etree.ElementTree as ET
import zipfile

CONSTRAINT_TYPES = {6: "Distance", 7: "DistanceX", 8: "DistanceY", 9: "Angle",
                    11: "Radius", 18: "Diameter", 19: "Weight"}
VALUE_TAGS = ("Float", "Integer", "Bool", "String")
SKIP_PROPS = {"Label2", "_ElementMapVersion", "Shape", "ExpressionEngine",
              "Placement", "Geometry", "Constraints", "ExternalGeo"}


def fmt(v):
    try:
        f = float(v)
    except ValueError:
        return v
    return f"{f:.6g}"


def prop_value(prop):
    ptype = prop.get("type", "")
    if "Link" in ptype:
        names = [e.get("value") or e.get("obj") for e in prop.iter()
                 if e.tag in ("Link", "LinkSub", "Sub") and (e.get("value") or e.get("obj"))]
        return "[" + ", ".join(names) + "]" if names else None
    if ptype.endswith("Enumeration"):
        el = prop.find("Integer")
        enums = [e.get("value") for e in prop.iter("Enum")]
        idx = int(el.get("value")) if el is not None else -1
        return enums[idx] if 0 <= idx < len(enums) else (el.get("value") if el is not None else None)
    for tag in VALUE_TAGS:
        el = prop.find(tag)
        if el is not None:
            return fmt(el.get("value"))
    return None


def main(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("Document.xml"))
    types = {o.get("name"): o.get("type") for o in root.find("Objects")}
    for obj in root.find("ObjectData"):
        name = obj.get("name")
        props = {p.get("name"): p for p in obj.iter("Property")}
        label = prop_value(props["Label"]) if "Label" in props else name
        print(f"== {name} [{types.get(name, '?')}] \"{label}\"")
        for pname in sorted(props):
            if pname in SKIP_PROPS or pname == "Label":
                continue
            val = prop_value(props[pname])
            if val not in (None, "", "[]"):
                print(f"   {pname} = {val}")
        for ex in obj.iter("Expression"):
            print(f"   expr {ex.get('path')} = {ex.get('expression')}")
        for cell in obj.iter("Cell"):
            alias = f" ({cell.get('alias')})" if cell.get("alias") else ""
            print(f"   cell {cell.get('address')}{alias} = {cell.get('content')}")
        others = 0
        for c in obj.iter("Constrain"):
            ctype = int(c.get("Type"))
            if ctype in CONSTRAINT_TYPES:
                val = float(c.get("Value"))
                shown = f"{math.degrees(val):.4g}deg" if ctype == 9 else f"{val:.6g}"
                cname = f" {c.get('Name')}" if c.get("Name") else ""
                print(f"   constraint {CONSTRAINT_TYPES[ctype]}{cname} = {shown}")
            else:
                others += 1
        if others:
            print(f"   constraints (geometric) = {others}")


if __name__ == "__main__":
    main(sys.argv[1])
