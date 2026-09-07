---
name: produce-forest-villa-episode
description: Generate or revise a complete 60-second, four-segment live-action episode for stories/forest-villa-apocalypse. Produces the fixed project structure, four-shot Chinese storyboards, Seedance-ready director prompts with 景别/构图/运镜手法/画面内容/台词, continuity records, and missing photoreal 16:9 no-person reference assets. Use when continuing this story, replacing weak or cryptic prompts, rebuilding segments, or completing scripts and assets before video generation.
---

# Produce Forest Villa Episode

Create one production-ready episode inside `stories/forest-villa-apocalypse/`. Treat scripts, visual assets, continuity, and API handoff as one deliverable.

## Read Context

Read in this order before editing:

1. `stories/forest-villa-apocalypse/AGENTS.md`
2. `docs/story-memory.md`, `docs/production-rules.md`, `docs/audience-strategy.md`, `docs/season-arc.md`
3. `docs/methods/douyin-short-drama-method.md` and `docs/contracts/video-api-handoff.md`
4. The previous episode's `episode.md`, `continuity.md`, `overview-storyboard.md`, `image-manifest.md`, and four `director-promt.txt` files
5. Relevant existing images under the story `assets/` tree

Read [references/episode-contract.md](references/episode-contract.md) before creating episode files. Read [references/director-prompt-and-assets.md](references/director-prompt-and-assets.md) before writing any segment prompt. Read [references/asset-reference-map.md](references/asset-reference-map.md) before selecting or generating images.

## Build The Episode

1. First write the plain-language episode chain: current state -> new practical problem -> action -> useful result -> cost or next risk. Resolve logic before splitting shots.
2. Convert the chain into four segment jobs: hook, preparation or limit, payoff, consequence. Each segment is one continuous 15-second event, not four unrelated illustrations.
3. Write exactly four shots per segment unless the user explicitly changes the format. Use `镜头一｜动作标题` through `镜头四｜动作标题`; never put seconds on individual shots.
4. Preserve this field order in every shot: `景别` -> `构图` -> `运镜手法` -> `画面内容` -> speaker and dialogue. Never collapse these fields into prose.
5. Give each shot one primary action and one narrative fact. Let the next shot begin from the physical state left by the previous shot.
6. Write normal spoken Chinese. In danger scenes, 白棠 asks only questions a reasonable viewer would ask at that moment and 许砚 answers concretely. In daily scenes, let them react, tease, hesitate, or leave things unsaid; do not force every reply to explain a plan.
7. Before splitting shots, write four beat cards: each card must state the character's immediate goal, what blocks it, the choice made under pressure, and the visible change by the next shot. If a card lacks a choice or a changed situation, it is exposition, not drama.
8. Use only as much dialogue as the beat needs: normally 3-6 spoken lines and 45-90 Chinese characters per segment. Leave room for visible movement. Use at most one short line per shot when driving, fighting, running, lifting, wearing a mask, or performing precise work. Remove duplicate narration of clearly visible actions.
9. Give each line a dramatic job, which may be factual or emotional: reveal a fact, state a cost, force a decision, show embarrassment, tease, deflect, comfort, or expose character judgment. Never turn dialogue into a checklist of equipment or a slogan detached from the moment.
10. In action episodes, write the scene as `goal -> obstacle -> temporary solution -> new cost`, not `information -> preparation -> information -> conclusion`. A rescue must contain an actual point of failure after the plan begins; the injured person must be hurt by a visible, established cause.
11. Give every face shot a performance path: `starting emotion -> one visible micro-action -> ending emotion`. Use physical evidence such as a tightened jaw, held breath, eyes shifting to a sound, a delayed blink, or a hand stopping mid-task; never write only “紧张/愤怒/害怕”. Reserve one short face-only shot per important turn when the emotional change can replace dialogue.
12. Put speech only in stable mouth-readable shots: one visible speaker, mouth unobscured, no sprinting, driving, fighting, lifting, turning away, or mask-covered lips. Keep a spoken line to one short sentence. Put radio lines over an object, route, or listener reaction so the model does not invent an absent speaker.
13. Treat the camera as part of the action: choose one motivated move and state its finish state. Use slow push-ins for a decision, over-the-shoulder long lens for two-person tension, locked-off framing plus off-screen sound for unseen danger, and follow-tracking only when the character is actually moving. Keep direction continuous across cuts (`exit right -> enter left`).
14. Use `scripts/build_ep008_014_accelerated.py` only for EP008. For the current EP009-EP016 fish-loop, doctor-rescue, and raider canon, use `scripts/build_ep009_016_raider_arc.py`; never run the deprecated `build_ep009_016.py`.
15. Keep upgrades costly. Attach at least one limit such as inventory use, power draw, payload, noise, maintenance, illness, weather, or exposure.
16. Create every required episode and segment file from the contract. Put runtime outputs only under each segment's `output/` directory.
17. Lock wardrobe independently from the digital-human face asset. Every segment with 许砚 must spell out `FVA_XU_YAN_OUTFIT_001`; every segment with 白棠 must spell out `FVA_BAI_TANG_OUTFIT_001`. Never rely on “same outfit” alone, because the asset's original clothing may leak into generation.
18. Treat draw cards as multi-episode dependencies. Before adding a new card, check the episode outline and continuity for unused cards, equipment, animals, materials, vehicles, or facilities. Reuse an existing resource whenever it can credibly solve the problem.
19. Do not use medicine as routine barter. Prefer renewable outputs or capacity such as filtered water, charging, vegetables, eggs, seedlings, seed stock, drone delivery, repair work, or information, and state the operating cost of each trade.

## Generate Assets

1. Audit existing assets before generating. Inspect the previous episode's `image-manifest.md`, the story asset folders, and relevant images with `view_image`.
2. Reuse the master villa three-view and recent modern assets as hard style references.
3. Make an asset responsibility table before generation: one image locks one main responsibility such as location, object design, construction state, route geometry, or exact animal count.
4. Generate only missing scene, structure, prop, vehicle, animal, and route images. Do not generate a new image when a current canonical asset already covers the same responsibility.
5. Use built-in `imagegen` by default. Generate distinct assets with distinct calls.
6. Make every new asset photoreal, `16:9`, modern, clearly readable, and free of people, hands, silhouettes, faces, and clothing. People belong only to Ark digital-human inputs.
7. Keep exact counts for count-sensitive assets such as animals, fuel cans, cargo cages, or zombies. Inspect and correct the generated image before using it.
8. Copy accepted images from `$CODEX_HOME/generated_images/` into the story asset tree. Never leave a referenced final only under `$CODEX_HOME`.
9. In each director prompt, describe every reference as `参考图N：...，只锁定...；图中没有人物。` State what it controls and what it must not control.
10. Update `image-manifest.md`, each `director-promt.txt` reference order, and each `api-request.md` after files exist. Do not create dangling asset paths.

## Prepare Video Handoff

- Use `asset://asset-20260320075237-29hdx` for 许砚.
- Use `asset://asset-20260320075131-k78qt` for 白棠.
- Use `asset://asset-20260310030618-88hlb` for 沈知夏 whenever she appears.
- Treat these assets as face/identity locks only. In every prompt, repeat the canonical outfit colors, layers, pants, and footwear from both character cards, and use the preceding segment tail frame as a wardrobe reference when available.
- Pass only the digitally locked characters who are physically visible in that segment through repeated `--digital-human` arguments. A single character may use `asset://...`; two or more visible characters must use `角色名=asset://...`. Text mentions do not lock a character, and an absent character's asset creates avoidable speaker ambiguity.
- Seedance 2.0-mini accepts at most nine image inputs in one request, and every digital-human `asset://` input counts toward that limit. Use at most three visible digital humans per segment, then fill the remaining slots with inspected no-person scene, wardrobe, hairstyle, prop, or effect references until the request contains exactly nine image inputs.
- Keep each shot to at most two clear people. Split a third character's reaction into a separate shot; never stage three or four clear faces in one frame. Do not submit a digital-human asset for a character who stays off screen.
- For two or more visible digital humans, submit each as `--digital-human "角色名=asset://..."` and declare the same role/asset pairs in an identity-lock header above `参考图1`. Digital humans do not consume `参考图N` numbers. Number only non-human inputs: preceding tail frame and other local images first, then hosted image URLs. Supply a matching label for every non-human reference.
- A signature hairstyle is not guaranteed by a face asset or an outfit flat lay. For 叶凝霜, reserve one non-human slot for an inspected faceless silver-white long-hair reference and require at least one clear frontal or three-quarter medium close-up. Do not combine an identity lock with an all-profile/all-distant-shot instruction.
- If the preceding tail frame is submitted, never omit it from the numbered prompt map. Do not force it into the request when its visible male identity conflicts with the next segment's main space; in that case omit it deliberately, document the reason in `api-request.md`, and rely on the relevant no-person scene anchor or split the spaces into separate single-character clips.
- Every line intended to be heard in the generated video needs a `说话者绑定：` instruction immediately before it: the named character, screen position, expression, visible unmasked mouth, and an explicit instruction that every other person remains silent. Do not rely on a name label alone.
- Do not place speech on a run, fight, vehicle maneuver, door-closing, impact, or masked shot. Use a short reaction shot with a single visible mouth, or generate clean action and add the assigned voice in post when the role-to-voice match matters.
- Inspect `output/api-request-payload.json` before accepting a submission; every on-screen character asset URL must appear as an independent `image_url` content part.
- Use `doubao-seedance-2-0-mini-260615`, `15s`, `16:9`, `480p`, and audio for draft requests unless the user overrides them.
- Select the no-person references by the segment's actual shots and use them to bring the digital-human plus reference-image total to exactly nine without exceeding the platform limit.
- Do not upload storyboard sheets.
- Run `scripts/ark_video.py submit ... --dry-run` for every segment. Accept the plan only when the strict reference-map check passes; inspect the resolved digital-human names and `参考图1..N` order before any paid submission.
- Submit paid video tasks only when the user explicitly asks to generate video.
- When the user asks for all four segments, submit strictly in order and never in parallel. Wait for Segment01 to finish, inspect representative frames and audio, then record `scripts/ark_video.py qa --status passed` before Segment02. Repeat for every boundary. If any segment has wrong identity, wrong wardrobe, extra people, broken action, wrong speaker/lip sync, severe garbled speech, or discontinuity, record `rejected` and stop; do not regenerate it and do not submit later segments unless the user gives a new instruction.

## Validate

Run:

```bash
python3 stories/forest-villa-apocalypse/skills/produce-forest-villa-episode/scripts/validate_episode.py \
  stories/forest-villa-apocalypse/episodes/<episode-dir>
```

Fix every reported missing file, missing reference, wrong ratio, or malformed shot before finishing. Report generated asset paths and whether video work stopped at dry-run or was formally submitted.

## Canon Guardrails

- No rebirth or complete future knowledge.
- No automatic building, instant farming, infinite payload, infinite power, or invincible equipment.
- Keep the modern three-story villa, cool gray/charcoal architecture, high wall, black gate, solar-storage-generator power system, and mountain setting.
- Keep outsiders outside the main house. Use radio, gate intercom, remote exchange, back view, or hands when no character asset exists.
- Keep zombies non-gory and increasingly strategic. They may react to sound, light, smell, routes, and routines.
- Turn every new resource into later work. Animals require water, feed, cleaning, illness control, breeding, manure handling, and noise management.
