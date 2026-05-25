"""
SnapLyrics Sync — Standalone LRC sync via Whisper transcription.

Sync-only CLI (no After Effects generation).
The full pipeline (sync + generate) is in snaplyrics.py.

Expects a _vocals file next to each audio file:
    Song Name.wav           # Audio
    Song Name_vocals.wav    # Vocals (same name + _vocals, same extension)
    Song Name.lrc           # Lyrics

Usage:
    python3 snaplyrics_sync.py <folder>
"""

import argparse
from pathlib import Path

from snaplyrics import (
    LrcParser, LrcSyncer, LrcWriter, _find_audio_files,
)


def main():
    parser = argparse.ArgumentParser(
        description="SnapLyrics Sync — transcribe _vocals and align with LRC lyrics"
    )
    parser.add_argument("folder", help="Folder with audio + .lrc + _vocals files")
    args = parser.parse_args()

    if not LrcSyncer.available():
        print("Missing dependencies. Install with:")
        print("  pip install openai-whisper")
        return

    folder = Path(args.folder)
    audio_files = _find_audio_files(folder)

    if not audio_files:
        print(f"No audio files found in {folder}")
        return

    # Filter to files that have a _vocals counterpart
    syncable = [(f, v) for f in audio_files
                if (v := LrcSyncer.find_vocals(f)) is not None]

    if not syncable:
        print(f"No _vocals files found. Expected pattern: Song_vocals.wav")
        return

    print(f"Folder: {folder}")
    print(f"  {len(audio_files)} audio files, {len(syncable)} with _vocals")
    print()

    lrc_parser = LrcParser()
    syncer = LrcSyncer()
    writer = LrcWriter()
    success = 0
    skipped = 0
    errors = 0

    for idx, (audio_file, vocals_file) in enumerate(syncable, 1):
        lrc_file = audio_file.with_suffix(".lrc")
        print(f"[{idx}/{len(syncable)}] {audio_file.stem}")

        if not lrc_file.exists():
            print(f"  No .lrc file, skipping")
            skipped += 1
            print()
            continue

        try:
            lyrics, metadata = lrc_parser.parse(lrc_file)
            if not lyrics:
                print(f"  No lyrics found in .lrc")
                skipped += 1
                print()
                continue

            synced, metadata, info = syncer.sync(
                audio_file, lyrics, metadata, vocals_file,
            )
            if info:
                writer.write(synced, metadata, lrc_file)
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  Error: {e}")
            errors += 1

        print()

    print(f"{'='*50}")
    print(f"Synced: {success}")
    if skipped:
        print(f"Skipped: {skipped}")
    if errors:
        print(f"Errors: {errors}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
