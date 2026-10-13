#!/bin/zsh
set -u
cd /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rift-breakers/episodes/OP00_opening/segment_01_00-30s/
export ARK_API_KEY=$(security find-generic-password -s codex-ark-api-key -w)
PY=/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/scripts/ark_video.py

shots=(
 "l01|01_l01_aerial-rift.png"
 "l02|02_l02_metro-reflection.png"
 "l03|03_l03_crowd-upstream.png"
 "l04|04_l04_sky-anomaly.png"
 "l05|05_l05_rooftop-mio.png"
 "l06|06_l06_mio-barrier.png"
 "l07|07_l07_akaji-leap.png"
 "l08|08_l08_yakumo-draw.png"
 "l09|09_l09_kirihara-monitor.png"
 "l10|10_l10_kokuyou-rooftop.png"
)

pids=()
for entry in "${shots[@]}"; do
  lid="${entry%%|*}"
  fn="${entry##*|}"
  mkdir -p "runs/$lid"
  (
    python3 "$PY" submit \
      --segment "runs/$lid" \
      --prompt-file "$PWD/promt_dir/prompt_${lid}.txt" \
      --image "$PWD/frame/$fn" \
      --duration 5 --ratio 16:9 --resolution 720p \
      --video-name raw.mp4 \
      --privacy-retry 2 \
      > "runs/$lid/submit.log" 2>&1
    echo "EXIT=$?" >> "runs/$lid/submit.log"
  ) &
  pids+=($!)
  echo "launched $lid pid=$!"
done

echo "waiting for ${#pids[@]} jobs..."
wait
echo "ALL_DONE"
for entry in "${shots[@]}"; do
  lid="${entry%%|*}"
  echo "== $lid =="
  tail -n 3 "runs/$lid/submit.log"
done
