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

    # Build list: find _vocals or mark for separation
    syncable = []
    for f in audio_files:
        v = LrcSyncer.find_vocals(f)
        if v:
            syncable.append((f, v))
        elif LrcSyncer.can_separate():
            syncable.append((f, None))  # will be separated

    if not syncable:
        print(f"No _vocals files found and demucs not installed.")
        print(f"  Provide Song_vocals.wav files or: pip install demucs")
        return

    print(f"Folder: {folder}")
    print(f"  {len(audio_files)} audio files, {sum(1 for _, v in syncable if v)} with _vocals")
    if any(v is None for _, v in syncable):
        print(f"  {sum(1 for _, v in syncable if v is None)} will be separated with Demucs")
    print()

    lrc_parser = LrcParser()
    syncer = LrcSyncer()
    writer = LrcWriter()
    success = 0
    skipped = 0
    errors = 0

    for idx, (audio_file, vocals_file) in enumerate(syncable, 1):
        lrc_file = audio_file.with_suffix(".lrc")
        txt_file = audio_file.with_suffix(".txt")
        print(f"[{idx}/{len(syncable)}] {audio_file.stem}")

        # Separate vocals if needed
        if vocals_file is None:
            try:
                vocals_file = LrcSyncer.separate_vocals(audio_file)
            except Exception as e:
                print(f"  Demucs error: {e}")
                errors += 1
                print()
                continue

        try:
            # Load reference lyrics if available (optional)
            reference = None
            if lrc_file.exists():
                reference, _ = lrc_parser.parse(lrc_file)
                print(f"  Reference: .lrc ({len(reference)} lines)")
            elif txt_file.exists():
                reference, _ = lrc_parser.parse_txt(txt_file)
                print(f"  Reference: .txt ({len(reference)} lines)")

            synced, info = syncer.sync(vocals_file, reference)
            if synced:
                output_lrc = audio_file.with_suffix(".lrc")
                writer.write(synced, [], output_lrc)
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
