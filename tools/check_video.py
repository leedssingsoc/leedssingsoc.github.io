"""Check a video before it goes on the website, so it can't play fast, freeze or drift out of sync.

Usage: python tools/check_video.py video.mp4 [original.mp4 --cut START END]

Always checks: H.264 + AAC, yuv420p, faststart (plays while downloading), even frame timing (no stutter), and that the picture and the
sound last the same time (within 0.1s). A mismatch is exactly the bug where a re-cut video runs fast and then
freezes while the sound carries on.
With an original and the cut range (seconds removed), also checks that frames after the cut match the original
at one steady offset, i.e. it plays at the real speed all the way through.
"""
import json
import subprocess
import sys


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,codec_name,pix_fmt,duration:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def frame(path, t):
    from PIL import Image
    import io
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                          "-vf", "scale=64:-1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(raw)).convert("L") if raw else None  # None: no picture at t (it froze/ended early)


def diff(a, b):
    from PIL import ImageChops, ImageStat
    if a is None or b is None:
        return 255.0
    return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]


def main(argv):
    if not argv:
        sys.exit(__doc__)
    path, problems = argv[0], []
    info = probe(path)
    streams = {s["codec_type"]: s for s in info["streams"]}
    v, a = streams.get("video"), streams.get("audio")
    if not v or v.get("codec_name") != "h264" or v.get("pix_fmt") != "yuv420p":
        problems.append("video must be H.264, yuv420p (re-encode with -c:v libx264 -pix_fmt yuv420p)")
    if a and a.get("codec_name") != "aac":
        problems.append("audio must be AAC (-c:a aac)")
    if v and a:
        dv, da = float(v.get("duration", 0)), float(a.get("duration", 0))
        print(f"picture {dv:.2f}s · sound {da:.2f}s")
        if abs(dv - da) > 0.1:
            problems.append(f"picture and sound lengths differ by {abs(dv - da):.2f}s: it will run fast/freeze or drift. "
                            "Cut with trim/atrim + concat (keeps real timestamps), never setpts=N/FRAME_RATE/TB.")
    if v:
        pts = sorted(float(x) for x in subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time", "-of", "csv=p=0", path],
            capture_output=True, text=True, check=True).stdout.split() if x.strip())
        gaps = [round((b - a) * 1000) for a, b in zip(pts, pts[1:])]
        if gaps:
            print(f"frame gaps {min(gaps)}-{max(gaps)} ms")
            if max(gaps) - min(gaps) > 5:
                problems.append("uneven frame timing (stutters/lags on screen). Even it out with "
                                "-vf setpts=N/<fps>/TB -r <fps>, where fps = frames ÷ duration (e.g. 20)")
    with open(path, "rb") as f:
        head = f.read(4096)
    if head.find(b"moov") == -1 or (head.find(b"mdat") != -1 and head.find(b"moov") > head.find(b"mdat")):
        problems.append("not faststart: re-encode with -movflags +faststart")

    if len(argv) == 5 and argv[2] == "--cut":
        orig, start, end = argv[1], float(argv[3]), float(argv[4])
        total = float(probe(orig)["format"]["duration"])
        times = [t for t in (end + 1.0, (end + total) / 2, total - 0.6) if end < t < total]
        refs = [frame(orig, t) for t in times]
        # the cut snaps to frames, so find the one offset that fits all check points, then judge the worst of them
        best = None
        for d in range(-25, 26):
            off = (end - start) + d / 100
            scores = [diff(r, frame(path, t - off)) for r, t in zip(refs, times)]
            if best is None or sum(scores) < sum(best[1]):
                best = (off, scores)
        offset, worst = best[0], max(best[1])
        print(f"cut offset {offset:.2f}s · worst frame difference after the cut {worst:.1f} (under 3 is a match)")
        if worst > 3:
            problems.append("frames after the cut don't line up with the original: the speed is wrong")

    if problems:
        print("NOT OK:\n- " + "\n- ".join(problems))
        sys.exit(1)
    print("OK: safe to publish")


if __name__ == "__main__":
    main(sys.argv[1:])
