# Asset Reference Map

## Canonical Anchors

Resolve these paths relative to `stories/forest-villa-apocalypse/` and inspect relevant images before generating:

| Purpose | Path |
| --- | --- |
| Master villa structure and palette | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-structure-three-view.png` |
| Modern villa exterior day | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-exterior-day-16x9.png` |
| Modern gate and intercom | `assets/props/references/outer-gate-trade-intercom-box-16x9.png` |
| Modern wall construction | `assets/scenes/SCENE_FOREST_VILLA_001/references/wall-manual-construction-background-modern-v2-16x9.png` |
| Modern tripwire sensor | `assets/props/references/wireless-tripwire-installation-background-modern-v2-16x9.png` |
| Modern basement storage | `assets/scenes/SCENE_FOREST_VILLA_001/references/basement-storage-function-test-high-tech-v3-16x9.png` |
| Modern empty poultry pen | `assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-empty-modern-16x9.png` |
| Heavy-lift cargo drone | `assets/vehicles/references/heavy-lift-agricultural-cargo-drone-16x9.png` |
| Diesel pickup | `assets/vehicles/references/diesel-pickup-supply-truck-16x9.png` |
| Groundwater system | `assets/water/references/groundwater-well-pump-system-16x9.png` |
| Ordinary infected canon | `assets/zombies/references/ordinary-infected-canonical-trio-16x9.png` |
| Climber infected canon | `assets/zombies/references/climber-infected-canonical-16x9.png` |
| Compact crossbow and 12 bolts | `assets/props/references/compact-crossbow-twelve-bolts-16x9.png` |

## Selection Rules

1. Use the most recent episode asset that shows the exact current construction state.
2. Use the master three-view whenever an outdoor image includes the villa, gate, wall, balcony, roof, courtyard, or overall palette.
3. Use recent modern versions instead of rustic legacy images.
4. Do not feed two contradictory versions of the same scene into one video request.
5. Use no-person backgrounds for scene locking. Add 许砚 and 白棠 only through their `asset://` references.
6. Keep local references to two or three per segment. Assign one responsibility to each image.
7. Any ordinary infected after EP006 must reuse the ordinary infected canon. Any climbing infected must reuse `FVA_ZOMBIE_CLIMBER_001`; do not redesign its face, clothes, build, or hardened fingers.

## Imagegen Prompt Requirements

Include `photorealistic-natural`, `16:9 live-action AI video reference`, the exact asset purpose and object counts, the cool-white/pale-gray/charcoal villa palette, and `absolutely no people or human body parts`.

Exclude text, logos, watermarks, anime, game CG, over-sharpening, fish-scale grids, and cluttered micro-detail.

For count-sensitive assets, state the count at least twice. Inspect the output manually. If the count is wrong, perform one precise edit that changes only the incorrect object.

## Asset Placement

- Scene and building state: `assets/scenes/SCENE_FOREST_VILLA_001/references/`
- Props and cargo: `assets/props/references/`
- Vehicles and drones: `assets/vehicles/references/`
- Water systems: `assets/water/references/`

Use descriptive lowercase kebab-case names ending in `-16x9.png`.
