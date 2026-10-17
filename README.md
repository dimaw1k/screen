# Screen Dot

A tiny, draggable floating screenshot button for Windows 10/11. Left-click the black circle to capture the primary display and copy the image directly to the Windows Clipboard. Paste it with Ctrl+V in Telegram, WhatsApp, Paint, Word, or another app.

## Use

- **Left-click** the dot: takes a screenshot and copies it to Clipboard.
- **Hold and drag** the dot: moves it to another place on the screen. Dragging does not take a screenshot.
- **Right-click** the dot: opens the Exit option.
- The dot briefly turns green after a successful capture.
- The dot hides during capture so it is not included in the screenshot.

## Run from source

1. Install Python 3.10 or newer from python.org and enable "Add Python to PATH".
2. Extract this project into a folder.
3. Double-click `run.bat`. It installs the dependency and starts the app.

## Build a standalone EXE

Double-click `build_exe.bat`. The resulting application will be at `dist/ScreenDot.exe`. The EXE can be copied to another Windows computer and does not require Python on that computer.

The app captures the primary display, normally the laptop's built-in screen. It does not automatically save screenshot files and does not upload screenshots anywhere.
