"""
Entry point for the osu! MapClassifier overlay.

Usage:
    python overlay/main.py

The overlay window appears in the top-right corner.
- Drag to reposition.
- Right-click to close.
"""
from __future__ import annotations

import queue
import sys
from pathlib import Path

# In a PyInstaller bundle, overlay/ is packed as the overlay package so
# detector and gui must be imported as overlay.detector / overlay.gui.
# When running from source, they live alongside this file and are imported directly.
if getattr(sys, "frozen", False):
    sys.path.insert(0, sys._MEIPASS)
    from overlay.detector import MapDetector
    from overlay.gui import OverlayWindow
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from detector import MapDetector
    from gui import OverlayWindow


def main() -> None:
    data_queue: queue.Queue = queue.Queue()

    detector = MapDetector(data_queue)
    detector.start()

    overlay = OverlayWindow(data_queue)
    overlay.run()   # blocks on tkinter mainloop


if __name__ == "__main__":
    main()
