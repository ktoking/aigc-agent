# EP028-EP032 Winter Asset Map

All images below are 16:9, photoreal, and person-free. Use them as space/prop anchors only; keep character identity in the digital-human assets and keep the villa residents limited to Xu Yan, Bai Tang, and Shen Zhixia.

## New Winter Anchors

| Asset ID | File | Use |
| --- | --- | --- |
| `FVA_WINTER_VILLA_DEFENSE_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-exterior-defense-line-16x9.png` | Snowy three-story villa, high wall, gate, and the single second-floor balcony turret. |
| `FVA_WINTER_ENERGY_SHED_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-energy-shed-cooling-loop-16x9.png` | Closed energy shed, exterior cooling-water bypass, circulation pump, and accessible east-side pipe run. |
| `FVA_WINTER_HEAT_LEAK_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-night-heat-leak-16x9.png` | Distant snowy night view showing limited window light and a thin heat-vapor plume. |
| `FVA_WINTER_BACK_MOUNTAIN_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-back-mountain-heat-drain-16x9.png` | Snowy back-mountain footpath, drainage channel, and discreet heat-drain outlet. |
| `FVA_WINTER_EAST_ICE_BARRICADE_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-east-ice-barricade-16x9.png` | Ice-and-snow barricade outside the east wall, partial turret sightline obstruction, and cooling pipe at ground level. |
| `FVA_WINTER_CONTROL_ROOM_COLD_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/villa-control-room-first-snow-cold-16x9.png` | Powered but unheated control room, frosted windows, cold exterior cameras, and the established monitoring desk. |
| `FVA_PRINTER_FLOOR_HEATING_PARTS_001` | `assets/props/FVA_INDUSTRIAL_METAL_PRINTER_001/references/industrial-printer-floor-heating-components-16x9.png` | Printer fabricating a floor-heating manifold and fittings, with the pump housing, insulation, and seals on the bench. |
| `FVA_GROUND_FLOOR_RADIANT_BUILD_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/villa-ground-floor-self-built-radiant-heating-16x9.png` | Lifted timber flooring, serpentine pipe loops, manifold, insulation, and recoverable floorboards. |
| `FVA_WINTER_GATE_TRANSFER_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-gate-transfer-hatch-16x9.png` | Closed winter gate, intercom, and low food-transfer hatch with empty foreground space. |
| `FVA_WINTER_RECON_CAMP_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/winter-crooked-tree-recon-camp-16x9.png` | Snowy crooked-tree route marker and empty distant forest-edge camp. |
| `FVA_HEAVY_DRONE_RADAR_001` | `assets/vehicles/references/heavy-lift-drone-radar-module-installed-16x9.png` | Same heavy-lift drone with installed underside radar module. |

## Existing Reusable Anchors

| Asset ID | File | Use |
| --- | --- | --- |
| `FVA_CONTROL_ROOM_NIGHT_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/villa-overnight-defense-control-room-16x9.png` | Control desk, monitors, radio, and night-window geometry. |
| `FVA_EVOLVED_DRAW_SYSTEM_001` | `assets/props/FVA_EVOLVED_DRAW_SYSTEM_001/references/evolved-daily-draw-three-choice-phone-16x9.png` | The same physical draw phone and three-choice card layout. |
| `FVA_INDUSTRIAL_METAL_PRINTER_001` | `assets/props/FVA_INDUSTRIAL_METAL_PRINTER_001/references/industrial-metal-printer-installed-utilities-16x9.png` | Garage-side printer and repair bay. |
| `FVA_AUTO_TURRET_001` | `assets/props/references/auto-defense-turret-balcony-radar-16x9.png` | The only automatic turret; it remains on the second-floor balcony. |
| `FVA_THERMAL_AFTER_DIVERSION_001` | `assets/scenes/SCENE_FOREST_VILLA_001/references/villa-thermal-signature-after-heat-diversion-16x9.png` | Heat-signature monitoring only, not a literal normal-camera color reference. |

## Segment Coverage

| Episode | Segment | Required anchors |
| --- | --- | --- |
| EP028 | 01 | `FVA_WINTER_CONTROL_ROOM_COLD_001`, `FVA_INDUSTRIAL_METAL_PRINTER_001`, `FVA_WINTER_ENERGY_SHED_001` |
| EP028 | 02 | `FVA_PRINTER_FLOOR_HEATING_PARTS_001`, `FVA_GROUND_FLOOR_RADIANT_BUILD_001`, `FVA_WINTER_ENERGY_SHED_001` |
| EP028 | 03 | `FVA_GROUND_FLOOR_RADIANT_BUILD_001`, `FVA_WINTER_ENERGY_SHED_001`, existing door/window anchor |
| EP028 | 04 | `FVA_GROUND_FLOOR_RADIANT_BUILD_001`, `FVA_WINTER_HEAT_LEAK_001`, `assets/vehicles/references/heavy-lift-agricultural-cargo-drone-16x9.png` |
| EP029 | 01 | `FVA_WINTER_GATE_TRANSFER_001`, `FVA_WINTER_VILLA_DEFENSE_001`, `FVA_WINTER_CONTROL_ROOM_COLD_001` |
| EP029 | 02 | `FVA_WINTER_GATE_TRANSFER_001`, `FVA_WINTER_HEAT_LEAK_001`, `FVA_WINTER_CONTROL_ROOM_COLD_001` |
| EP029 | 03 | `FVA_WINTER_CONTROL_ROOM_COLD_001`, ordinary camera-drone anchor, `FVA_WINTER_RECON_CAMP_001` |
| EP029 | 04 | `FVA_WINTER_CONTROL_ROOM_COLD_001`, `FVA_WINTER_VILLA_DEFENSE_001`, `FVA_AUTO_TURRET_001` |
| EP030 | 01-02 | `FVA_WINTER_VILLA_DEFENSE_001`, `FVA_WINTER_HEAT_LEAK_001`, `FVA_CONTROL_ROOM_NIGHT_001` |
| EP030 | 03-04 | `FVA_WINTER_EAST_ICE_BARRICADE_001`, `FVA_WINTER_ENERGY_SHED_001`, `FVA_CONTROL_ROOM_NIGHT_001` |
| EP031 | 01-02 | `FVA_WINTER_EAST_ICE_BARRICADE_001`, `FVA_WINTER_ENERGY_SHED_001`, `FVA_AUTO_TURRET_001`, `FVA_CONTROL_ROOM_NIGHT_001` |
| EP031 | 03-04 | `FVA_WINTER_ENERGY_SHED_001`, `FVA_WINTER_EAST_ICE_BARRICADE_001`, existing gate anchor, `FVA_AUTO_TURRET_001` |
| EP032 | 01-02 | `FVA_WINTER_EAST_ICE_BARRICADE_001`, `FVA_WINTER_ENERGY_SHED_001`, `FVA_CONTROL_ROOM_NIGHT_001` |
| EP032 | 03 | `FVA_CONTROL_ROOM_NIGHT_001`, existing gate/intercom anchor |
| EP032 | 04 | `FVA_CONTROL_ROOM_NIGHT_001`, `FVA_HEAVY_DRONE_RADAR_001`, `FVA_WINTER_BACK_MOUNTAIN_001` |

## Generation Guardrails

- Do not use more than three shared scene/prop references in a 15-second request; add a first or last frame only when continuity needs it.
- Do not use a scene image to lock a character face. Digital-human assets lock faces; each request still states the outfit.
- `FVA_WINTER_EAST_ICE_BARRICADE_001` is exterior-only: no person belongs inside the wall, and the barricade never becomes a second wall or enters the courtyard.
- The turret is singular in every shot. Do not duplicate it in wide angles, reflections, or monitor feeds.
