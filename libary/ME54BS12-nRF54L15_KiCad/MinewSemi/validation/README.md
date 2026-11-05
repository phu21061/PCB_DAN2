# Validation — 2026-11-04

Validated with KiCad 10.0.3 installed on this machine.

- Parsed the original manufacturer PDF pin tables independently with pypdf: all 39 generated symbol pin numbers and names match. Counted 29 GPIO and 5 separate GND pads.
- Loaded the footprint through native pcbnew: exactly 39 unique SMD pads and one antenna rule area covering all 32 potential copper layers.
- Exported symbol and footprint through kicad-cli to SVG, rendered PNG previews, and visually inspected both.
- Built an isolated four-layer PCB containing one front-side and one back-side instance, each with unique pad nets, and a board outline. Native DRC: **0 violations, 0 unconnected items**. This checks geometry and clearances; it does not validate an application circuit.
- Negative control: inserted four tracks in the front footprint's antenna region, one on each of F.Cu, In1.Cu, In2.Cu and B.Cu. DRC correctly returned four `items_not_allowed` errors. The same tracks also produce four expected dangling-track warnings.
- The check PCB was separate from TPV3. TPV3 schematic/board contents were not edited.

The JSON reports accompany this file. No physical soldering, RF test or manufacturing validation has been performed. Host land dimensions are the documented design choices in README.vi.md.
