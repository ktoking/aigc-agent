#!/usr/bin/env python3
"""Re-edit wasteline EP001: trim long static shots, output trimmed segments."""
import subprocess, re, os, tempfile

BASE = "/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/wasteline/episodes/EP001_wasteline"
MAX_SHOT = 9.0  # max seconds per shot
MIN_SHOT = 0.5  # merge shots shorter than this into previous

SEGMENTS = [
    "segment_01_00-30s", "segment_02_30-60s", "segment_03_60-90s",
    "segment_04_90-120s", "segment_05_120-150s", "segment_06_150-180s",
    "segment_07_180-210s", "segment_08_210-240s",
]

def get_duration(f):
    return float(subprocess.check_output(
        ['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]
    ).decode().strip())

def detect_scenes(f, threshold=0.12):
    cmd = ['ffmpeg','-i',f,'-filter:v',f"select='gt(scene,{threshold})',showinfo",'-f','null','-']
    r = subprocess.run(cmd, capture_output=True, text=True)
    times = sorted([float(m) for m in re.findall(r'pts_time:([0-9.]+)', r.stderr)])
    return times

def merge_short_shots(boundaries, dur):
    """Merge shots shorter than MIN_SHOT into previous shot."""
    result = [0.0]
    for t in boundaries:
        if t - result[-1] < MIN_SHOT and len(result) > 1:
            continue  # skip this boundary, merge with previous
        result.append(t)
    if abs(result[-1] - dur) > 0.1:
        result.append(dur)
    return result

def trim_segment(seg_name):
    input_f = os.path.join(BASE, seg_name, "output", "video.mp4")
    output_f = os.path.join(BASE, "trimmed", f"{seg_name}_trimmed.mp4")
    os.makedirs(os.path.join(BASE, "trimmed"), exist_ok=True)

    dur = get_duration(input_f)
    scenes = detect_scenes(input_f)
    boundaries = merge_short_shots(scenes, dur)

    # Build list of (start, end) for each shot, trimming long ones
    shots = []
    total = 0.0
    for i in range(len(boundaries)-1):
        start = boundaries[i]
        end = boundaries[i+1]
        shot_dur = end - start
        if shot_dur > MAX_SHOT:
            end = start + MAX_SHOT
            shot_dur = MAX_SHOT
        shots.append((start, end))
        total += shot_dur

    print(f"{seg_name}: original={dur:.2f}s, shots={len(shots)}, trimmed_total={total:.2f}s")
    for i, (s, e) in enumerate(shots):
        print(f"  shot {i+1}: {s:.2f}-{e:.2f} ({e-s:.2f}s)")

    # Extract each shot and concatenate
    tmpdir = tempfile.mkdtemp()
    shot_files = []
    for i, (start, end) in enumerate(shots):
        shot_f = os.path.join(tmpdir, f"shot_{i:02d}.mp4")
        cmd = [
            'ffmpeg', '-y', '-ss', str(start), '-to', str(end),
            '-i', input_f,
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
            '-c:a', 'aac', '-b:a', '192k',
            '-avoid_negative_ts', 'make_zero',
            shot_f
        ]
        subprocess.run(cmd, capture_output=True)
        shot_files.append(shot_f)

    # Concatenate shots
    list_f = os.path.join(tmpdir, "concat.txt")
    with open(list_f, 'w') as f:
        for sf in shot_files:
            f.write(f"file '{sf}'\n")

    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_f,
        '-c', 'copy', output_f
    ]
    subprocess.run(cmd, capture_output=True)

    out_dur = get_duration(output_f)
    print(f"  -> output: {out_dur:.2f}s")
    return output_f, out_dur

if __name__ == "__main__":
    results = []
    for seg in SEGMENTS:
        f, d = trim_segment(seg)
        results.append((seg, f, d))
    total = sum(d for _, _, d in results)
    print(f"\nTotal trimmed duration: {total:.2f}s ({total/60:.2f}min)")
