---
name: ai-microdrama-episode-production
description: Generate or update structured episodes for this AI microdrama project. Use when asked to create EP003/EP004 or any new episode, continue the story from an existing episode, produce episode.md/continuity.md/overview-storyboard.md/segment files, or preserve the project's character, asset, first-frame/last-frame, and video prompt format.
---

# AI Microdrama Episode Production

## Required Context

Before writing an episode, read these project files:

1. `docs/story-memory.md`
2. `docs/workflow.md`
3. `assets/style/global-style.md`
4. `assets/style/camera-language.md`
5. `assets/style/negative-prompts.md`
6. The previous episode's `episode.md`, `continuity.md`, and `overview-storyboard.md`
7. Relevant character cards in `assets/characters/*/00-character-card.md`
8. Relevant scene and prop cards in `assets/scenes/*/scene-card.md` and `assets/props/*/prop-card.md`
9. Templates in `templates/`

If the user provides only an episode number, infer the previous episode from `episodes/` and continue from its ending hook.

## Production Rules

- Produce one 60-second vertical episode split into 4 segments of 15 seconds or less.
- Keep the fixed directory shape:

```text
episodes/EPXXX_slug/
  episode.md
  continuity.md
  overview-storyboard.md
  segment_01_00-15s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    frames/
    output/
  segment_02_15-30s/
  segment_03_30-45s/
  segment_04_45-60s/
```

- Follow the exact field structure used by EP001 and EP002 unless the user asks for a format change.
- Keep every episode high-tension: opening hook in the first 5 seconds, at least one reversal/reveal/satisfying payoff, and a clear next-episode cliffhanger.
- Use short, sharp dialogue. Avoid idle exposition.
- Limit each episode to 2-3 practical scenes when possible.
- Maintain first-frame/last-frame continuity:
  - Segment 02 first frame inherits Segment 01 last frame.
  - Segment 03 first frame inherits Segment 02 last frame.
  - Segment 04 first frame inherits Segment 03 last frame, unless a clear transition is written.

## Character Locks

- `assets/characters/double-hero-final-reference.png` has highest priority for both heroines.
- `LIN_WAN_001` must match the left-side character: black extra-long straight hair, cool refined face, pale skin, faint mole under the left eye, calm and protective.
- `SHEN_QINGXUE_001` must match the right-side character: short hair between jaw and collarbone, air bangs, white outfit direction, warm but mature and firm.
- `GU_JINGCHEN_001` should look like a refined business elite first. Show danger through eyes, control, and information asymmetry, not cartoon villain behavior.
- Never redesign faces, hair, age, or core temperament.

## Episode Design Pattern

Use this sequence for each new episode:

1. **Continue the hook**: Start from the previous episode's final frame or unresolved question.
2. **Define this episode's job**: Pick one core dramatic purpose, such as stockpiling, finding Shen Qingxue, exposing Gu Jingchen, unlocking space base, or defending survivors.
3. **Build four beats**:
   - Segment 01: hook and immediate conflict.
   - Segment 02: choice, plan, or emotional pressure.
   - Segment 03: payoff, reversal, or power display.
   - Segment 04: consequence and next hook.
4. **Write files**:
   - `episode.md`: story intent, character roles, emotional curve, dialogue, titles.
   - `continuity.md`: previous-episode bridge, fixed states, character continuity, segment bridges, forbidden drift.
   - `overview-storyboard.md`: 60-second director overview and total prompt.
   - Segment files: `storyboard.md`, `first-frame.md`, `last-frame.md`, `prompt.md`.
5. **Self-check**:
   - Character references are named.
   - Scene IDs and prop IDs are used where relevant.
   - Each segment has clear first/last frame continuity.
   - Video prompts include ratio, duration, style, character locks, action, dialogue, audio, and negatives.
   - Ending hook naturally motivates the next episode.

## Style References

For external genre logic, use these principles without copying plot text:

- Vertical short drama favors one clear emotional beat per segment and tight phone-screen composition.
- AI motion comic workflows should remain asset-first: characters -> scene -> storyboard -> keyframes -> video.
- Apocalypse stockpiling stories work best when practical survival details become emotional security and power fantasy.

For the current reference notes and production checklist, read `references/episode-format.md` when generating or reviewing a full episode.
