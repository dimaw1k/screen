# Screen Dot

A minimal floating screenshot button for Windows 10/11. Click the small black circle to capture the primary display and copy the image directly to Clipboard. Then paste it with Ctrl+V in Telegram, WhatsApp, Paint, Word, or another app.

## Run from source

1. Install Python 3.10 or newer from python.org and enable Add Python to PATH.
2. Extract this project into a folder.
3. Double-click run.bat. It installs the dependency and starts the app.

## Build a standalone EXE

Double-click build_exe.bat. The resulting application will be at dist/ScreenDot.exe. The EXE can be copied to another Windows computer and does not require Python on that computer.

## Use

- Left-click the black circle: captures the primary display and copies the image to Clipboard.
- Right-click the circle: opens the Exit option.
- The circle briefly turns green after a successful capture.
- The circle hides during capture so it is not included in the screenshot.

This minimal version captures the primary display, normally the laptop's built-in screen. It does not automatically save screenshot files and does not upload screenshots anywhere.
