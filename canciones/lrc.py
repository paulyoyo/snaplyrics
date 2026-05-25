"""Thin wrapper -- runs SnapLyricsPipeline on this folder."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from snaplyrics import SnapLyricsPipeline

if __name__ == "__main__":
    pipeline = SnapLyricsPipeline(source_folder=Path(__file__).parent)
    pipeline.process_all_songs()
