"""
SnapLyrics — Convert rendered ProRes videos to HAP codec.

HAP is GPU-decoded, giving near-zero CPU usage during playback.
Ideal for openFrameworks, Resolume, VDMX, and any real-time video engine.

Usage:
    python3 convert_to_hap.py <folder>
    python3 convert_to_hap.py <folder> --codec hapq
    python3 convert_to_hap.py <folder> --codec hapalpha
"""

import argparse
import subprocess
import sys
from pathlib import Path


def _hex(h):
    r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"

_RESET = "\033[0m"
_BOLD = "\033[1m"
_LILAC = _hex("8956BA")
_SNOW = _hex("F7F7F5")
_GOLD = _hex("EAD82F")
_WISTERIA = _hex("C599E2")
_RED = "\033[38;2;220;60;60m"

CODECS = {
    "hap": {"encoder": "hap", "label": "HAP", "suffix": "_hap"},
    "hapq": {"encoder": "hap", "label": "HAP Q", "suffix": "_hap", "extra": ["-compressor", "snappy"]},
    "hapalpha": {"encoder": "hap", "label": "HAP Alpha", "suffix": "_hap", "extra": ["-compressor", "snappy", "-format", "rgba"]},
    "mjpeg": {"encoder": "mjpeg", "label": "MJPEG (fallback)", "suffix": "_mjpeg", "extra": ["-q:v", "2"]},
    "h264": {"encoder": "h264_videotoolbox", "label": "H.264 VideoToolbox", "suffix": "_h264",
             "extra": ["-b:v", "20M", "-profile:v", "high"]},
}


def check_encoder(encoder_name):
    """Check if ffmpeg has a specific encoder available."""
    result = subprocess.run(
        ["ffmpeg", "-encoders"], capture_output=True, text=True
    )
    return encoder_name in result.stdout


def find_mov_files(folder):
    output_dir = Path(folder) / "OUTPUT"
    if not output_dir.exists():
        print(f"{_RED}  OUTPUT folder not found in {folder}{_RESET}")
        return []
    movs = []
    for song_dir in sorted(output_dir.iterdir()):
        if not song_dir.is_dir():
            continue
        for f in song_dir.iterdir():
            if f.suffix.lower() == ".mov" and not any(
                s in f.stem for s in ("_hap", "_mjpeg", "_h264")
            ):
                movs.append(f)
    return movs


def convert(mov_path, codec_key):
    codec = CODECS[codec_key]
    suffix = codec["suffix"]
    out_path = mov_path.with_name(f"{mov_path.stem}{suffix}.mov")

    if out_path.exists():
        print(f"{_WISTERIA}    Already exists, skipping{_RESET}")
        return True

    cmd = [
        "ffmpeg", "-y", "-i", str(mov_path),
        "-c:v", codec["encoder"],
        "-an",
    ]
    cmd.extend(codec.get("extra", []))
    cmd.append(str(out_path))

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{_RED}    ffmpeg error: {result.stderr.strip()[-200:]}{_RESET}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="SnapLyrics — Convert rendered videos for real-time playback (HAP, MJPEG, H.264)"
    )
    parser.add_argument("folder", help="Folder containing the OUTPUT directory")
    parser.add_argument(
        "--codec", choices=list(CODECS.keys()), default=None,
        help="Codec: hap (default), hapq, hapalpha, mjpeg, h264. Auto-detects best available if omitted."
    )
    args = parser.parse_args()

    # Check ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"{_RED}  ffmpeg not found. Install with: brew install ffmpeg{_RESET}")
        return

    # Auto-detect best codec if not specified
    if args.codec:
        codec_key = args.codec
    elif check_encoder("hap"):
        codec_key = "hap"
    elif check_encoder("h264_videotoolbox"):
        codec_key = "h264"
    else:
        codec_key = "mjpeg"

    codec = CODECS[codec_key]

    # Warn if HAP not available
    if codec_key in ("hap", "hapq", "hapalpha") and not check_encoder("hap"):
        print(f"{_RED}  HAP encoder not available in your ffmpeg build{_RESET}")
        print(f"{_WISTERIA}  To enable HAP, rebuild ffmpeg with libsnappy:{_RESET}")
        print(f"{_WISTERIA}    brew install snappy && brew reinstall --build-from-source ffmpeg{_RESET}")
        print(f"{_SNOW}  Falling back to H.264 VideoToolbox...{_RESET}\n")
        codec_key = "h264" if check_encoder("h264_videotoolbox") else "mjpeg"
        codec = CODECS[codec_key]

    print(f"\n{_BOLD}{_LILAC}  SnapLyrics — Video Converter{_RESET}")
    print(f"{_LILAC}  ─────────────────────────────────{_RESET}")
    print(f"{_SNOW}  Codec:  {_GOLD}{codec['label']}{_RESET}")
    print(f"{_SNOW}  Source: {_WISTERIA}{args.folder}/OUTPUT{_RESET}\n")

    movs = find_mov_files(args.folder)
    if not movs:
        print(f"{_RED}  No .mov files found in OUTPUT subfolders{_RESET}")
        return

    print(f"{_SNOW}  Found {_GOLD}{len(movs)}{_SNOW} videos to convert{_RESET}\n")

    success = 0
    errors = 0

    for idx, mov in enumerate(movs, 1):
        # Progress bar
        pct = idx / len(movs)
        filled = int(30 * pct)
        bar = f"{_GOLD}{'█' * filled}{_WISTERIA}{'░' * (30 - filled)}{_RESET}"
        sys.stdout.write(f"\r  {bar} {_SNOW}{idx}/{len(movs)}{_RESET}")
        sys.stdout.flush()
        if idx >= len(movs):
            sys.stdout.write("\n")

        song_name = mov.parent.name
        print(f"{_LILAC}  [{idx}/{len(movs)}]{_SNOW} {song_name}{_RESET}")

        # Get file size for info
        size_mb = mov.stat().st_size / (1024 * 1024)
        print(f"{_WISTERIA}    {mov.name} ({size_mb:.0f} MB){_RESET}")

        if convert(mov, codec_key):
            suffix = codec["suffix"]
            out_path = mov.with_name(f"{mov.stem}{suffix}.mov")
            out_size = out_path.stat().st_size / (1024 * 1024)
            print(f"{_GOLD}    Converted → {out_path.name} ({out_size:.0f} MB){_RESET}")
            success += 1
        else:
            errors += 1

    print(f"\n{_LILAC}  {'━' * 40}{_RESET}")
    print(f"{_BOLD}{_GOLD}  HAP CONVERSION COMPLETE{_RESET}")
    print(f"{_LILAC}  {'━' * 40}{_RESET}")
    print(f"{_GOLD}  Converted: {success}{_RESET}")
    if errors:
        print(f"{_RED}  Errors: {errors}{_RESET}")
    print()


if __name__ == "__main__":
    main()
