"""Generate the project-local ME54BS12 library. Standard-library Python only.

Dimensions are in mm. PCB coordinates are TOP VIEW, antenna toward negative Y.
Source: MinewSemi ME54BS12-nRF54L15 Datasheet K EN, v1.0.0, 2025-08-07.
"""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent
PART = "ME54BS12-nRF54L15"
URL = "https://en.minewsemi.com/file/ME54BS12-nRF54L15_Datasheet_K_EN.pdf"
PIN_NAMES = {
    "1": "RF", "2": "P1.11", "3": "P1.12", "4": "P1.13",
    "5": "P1.14", "6": "P1.03", "7": "P1.02", "8": "P1.06",
    "9": "P1.05", "10": "VCC", "11": "GND", "12": "P0.00",
    "13": "P0.01", "14": "P0.02", "15": "P0.03", "16": "SWDIO",
    "17": "SWCLK", "18": "NRESET",
    "A1": "GND", "A5": "GND", "A6": "P0.04",
    "B1": "P1.09", "B5": "GND", "B6": "P2.09",
    "C1": "P1.10", "C5": "GND", "C6": "P2.10",
    "D1": "P2.00", "D5": "P2.08", "D6": "P2.07",
    "E1": "P1.08", "E5": "P2.05", "E6": "P2.06",
    "F1": "P1.07", "F2": "P1.04", "F3": "P2.01",
    "F4": "P2.03", "F5": "P2.02", "F6": "P2.04",
}


def num(v):
    return f"{v:.4f}".rstrip("0").rstrip(".") if v else "0"


def q(v):
    return json.dumps(str(v), ensure_ascii=False)


def pin_type(name):
    if name in ("VCC", "GND"):
        return "power_in"
    if name in ("SWCLK", "NRESET"):
        return "input"
    return "passive" if name == "RF" else "bidirectional"


def make_symbol():
    effects = "(effects (font (size 1.27 1.27)))"
    props = []
    for name, value, y, hidden in [
        ("Reference", "U", 34.29, False),
        ("Value", PART, 31.75, False),
        ("Footprint", f"MinewSemi:{PART}", 0, True),
        ("Datasheet", URL, 0, True),
        ("Description", "MinewSemi nRF54L15 radio module, 39 pads, PCB antenna", 0, True),
        ("ki_keywords", "MinewSemi ME54BS12 nRF54L15 Bluetooth BLE module", 0, True),
        ("ki_fp_filters", "ME54BS12*", 0, True),
    ]:
        ef = "(effects (font (size 1.27 1.27))" + (" hide)" if hidden else ")")
        props.append(f"    (property {q(name)} {q(value)} (at 0 {num(y)} 0) {ef})")
    pins = []

    def add(number, x, y, angle):
        name = PIN_NAMES[number]
        shown = "~{RESET}" if name == "NRESET" else name
        pins.append(f"      (pin {pin_type(name)} line (at {num(x)} {num(y)} {angle}) (length 2.54)\n"
                    f"        (name {q(shown)} {effects}) (number {q(number)} {effects}))")

    add("10", 0, 27.94, 270)
    by_name = {v: k for k, v in PIN_NAMES.items() if v != "GND"}
    for i in range(5):
        add(by_name[f"P0.{i:02}"], -15.24, 22.86 - i * 2.54, 0)
    for i in range(2, 15):
        add(by_name[f"P1.{i:02}"], -15.24, 7.62 - (i - 2) * 2.54, 0)
    for i in range(11):
        add(by_name[f"P2.{i:02}"], 15.24, 22.86 - i * 2.54, 180)
    for number, y in [("16", -7.62), ("17", -10.16), ("18", -12.7), ("1", -17.78)]:
        add(number, 15.24, y, 180)
    for i, number in enumerate(["11", "A1", "A5", "B5", "C5"]):
        add(number, -10.16 + i * 5.08, -33.02, 90)
    assert len(pins) == 39
    return (f'(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'
            f'  (symbol {q(PART)} (pin_names (offset 0.508)) (in_bom yes) (on_board yes)\n'
            + "\n".join(props)
            + f'\n    (symbol {q(PART + "_0_1")}\n'
            + '      (rectangle (start -12.7 25.4) (end 12.7 -30.48)\n'
            + '        (stroke (width 0.254) (type default)) (fill (type background))))\n'
            + f'    (symbol {q(PART + "_1_1")}\n'
            + "\n".join(pins) + ")\n  )\n)\n")


def pad_positions():
    pads = []
    # Body: x +/-6, y +/-7.9. Lowest side-pad centre is 0.7 above bottom.
    # 0.8 mm module land + 1.2 mm outward toe = 2.0 mm host land.
    for i in range(9):
        y = round(7.2 - (8 - i) * 1.27, 4)
        pads += [(str(i + 1), -6.2, y, 2.0, 0.8, "roundrect"),
                 (str(18 - i), 6.2, y, 2.0, 0.8, "roundrect")]
    # The mechanical drawing's bottom view is mirrored to the labelled top view.
    # Column 1 is 2.05 from LEFT in top view; column spacing is 1.5.
    # Row F is 1.4 above bottom; row spacing is 1.8.
    for ri, row in enumerate("ABCDEF"):
        for col in (range(1, 7) if row == "F" else [1, 5, 6]):
            pads.append((f"{row}{col}", round(-3.95 + (col - 1) * 1.5, 4),
                         round(-2.5 + ri * 1.8, 4), 0.8, 0.8, "circle"))
    assert {p[0] for p in pads} == set(PIN_NAMES)
    return pads


def make_footprint(pads):
    lines = [f'(footprint {q(PART)} (version 20240108) (generator "pcbnew")',
             '  (layer "F.Cu")',
             f'  (descr {q("MinewSemi ME54BS12-nRF54L15; 12x15.8mm; 39 pads; top view; " + URL)})',
             '  (tags "MinewSemi ME54BS12 nRF54L15 Bluetooth BLE module")',
             '  (attr smd)',
             '  (property "Reference" "REF**" (at 0 8.9 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',
             f'  (property "Value" {q(PART)} (at 0 10.3 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))']

    def line(a, b, layer, width=0.1, style="solid"):
        lines.append(f'  (fp_line (start {num(a[0])} {num(a[1])}) (end {num(b[0])} {num(b[1])}) '
                     f'(stroke (width {num(width)}) (type {style})) (layer {q(layer)}))')

    def poly(points, layer, width=0.1):
        for a, b in zip(points, points[1:] + points[:1]):
            line(a, b, layer, width)

    # Fabrication outline, chamfer adjacent to pin 1.
    poly([(-6, -7.9), (6, -7.9), (6, 7.9), (-6, 7.9),
          (-6, -2.3), (-5.5, -2.96), (-6, -3.62)], "F.Fab")
    line((-6, -3.84), (6, -3.84), "F.Fab", style="dash")
    lines.append('  (fp_text user "${REFERENCE}" (at 0 1.2 90) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    lines.append('  (fp_text user "ANTENNA" (at 0 -5.8 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    # Silk avoids the side pads and mask openings.
    for a, b in [((-6.12, -3.7), (-6.12, -8.02)), ((-6.12, -8.02), (6.12, -8.02)),
                 ((6.12, -8.02), (6.12, -3.7)), ((-6.12, 7.85), (-6.12, 8.02)),
                 ((-6.12, 8.02), (6.12, 8.02)), ((6.12, 8.02), (6.12, 7.85))]:
        line(a, b, "F.SilkS", 0.12)
    poly([(-7.7, -2.96), (-8.3, -3.26), (-8.3, -2.66)], "F.SilkS", 0.12)
    # Physical assembly courtyard; RF clearance is a separate rule area below.
    poly([(-6.25, -8.15), (6.25, -8.15), (6.25, -3.65),
          (7.45, -3.65), (7.45, 8.15), (-7.45, 8.15),
          (-7.45, -3.65), (-6.25, -3.65)], "F.CrtYd", 0.05)
    poly([(-10, -11.9), (10, -11.9), (10, -3.84), (-10, -3.84)], "Dwgs.User", 0.1)
    lines.append('  (fp_text user "ANTENNA: NO COPPER / COMPONENTS" (at 0 -10.5 0) (layer "Dwgs.User") (effects (font (size 0.65 0.65) (thickness 0.1))))')
    lines.append('  (fp_text user "4mm clearance at sides and antenna tip" (at 0 -9.3 0) (layer "Dwgs.User") (effects (font (size 0.6 0.6) (thickness 0.1))))')
    for number, x, y, w, h, shape in pads:
        extra = " (roundrect_rratio 0.125)" if shape == "roundrect" else " (solder_paste_margin_ratio -0.05)"
        lines.append(f'  (pad {q(number)} smd {shape} (at {num(x)} {num(y)}) '
                     f'(size {num(w)} {num(h)}) (layers "F.Cu" "F.Paste" "F.Mask")'
                     f' (solder_mask_margin 0.05){extra})')
    # Include every possible copper layer so later 4/6-layer boards stay protected.
    layers = '"F.Cu" "B.Cu" ' + " ".join(f'"In{i}.Cu"' for i in range(1, 31))
    lines.append(f'''  (zone (net 0) (net_name "") (layers {layers})
    (name "Antenna_4mm_clearance") (hatch edge 0.5)
    (connect_pads (clearance 0)) (min_thickness 0.25)
    (keepout (tracks not_allowed) (vias not_allowed) (pads not_allowed)
      (copperpour not_allowed) (footprints not_allowed))
    (fill (thermal_gap 0.3) (thermal_bridge_width 0.3))
    (polygon (pts (xy -10 -11.9) (xy 10 -11.9) (xy 10 -3.84) (xy -10 -3.84))))''')
    return "\n".join(lines) + "\n)\n"


def main():
    pretty = ROOT / "MinewSemi.pretty"
    pretty.mkdir(exist_ok=True)
    pads = pad_positions()
    (ROOT / "MinewSemi.kicad_sym").write_text(make_symbol(), encoding="utf-8")
    (pretty / f"{PART}.kicad_mod").write_text(make_footprint(pads), encoding="utf-8")
    with (ROOT / f"{PART}_pinmap.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Pad", "Signal", "Electrical_type", "X_mm_top_view", "Y_mm_top_view", "Pad_width_mm", "Pad_height_mm"])
        for number, x, y, w, h, _ in pads:
            writer.writerow([number, PIN_NAMES[number], pin_type(PIN_NAMES[number]), x, y, w, h])
    print("Created symbol and footprint: 39 matching pins/pads, 29 GPIO.")


if __name__ == "__main__":
    main()
