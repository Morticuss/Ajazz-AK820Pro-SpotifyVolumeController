# Spotify Volume Controller for Ajazz AK820 Pro

A lightweight Windows tool that redirects your Ajazz AK820 Pro keyboard's volume knob to control Spotify's volume independently, leaving your system volume untouched.

## What it does

Your keyboard's volume knob normally adjusts the entire system volume. This tool intercepts those volume commands and applies them only to Spotify through the Windows audio mixer, so you can adjust music volume without affecting game audio, Discord, or other applications.

## Features

- Controls only Spotify's volume via the keyboard knob
- Runs silently in the background
- Minimal resource usage
- All other keyboard functions work normally
- Works with any application that sends standard media volume keys

## Installation

### Option 1: Download the executable
1. Download `spotifyvol.exe` from the [releases page](../../releases)
2. Run the executable
3. (Optional) Add to Windows startup folder for automatic launch

### Option 2: Run from source
1. Clone the repository
2. Install dependencies: `pip install pynput pycaw comtypes`
3. Run: `python spotifyvol.py`

## Building from source

```bash
pyinstaller --onefile --noconsole spotifyvol.py
```

The executable will be in the `dist` folder.

## Usage

- Run the program (Spotify must be open)
- Twist your volume knob to adjust Spotify volume
- System volume remains unchanged

## License

MIT License - free to use, modify, and distribute.
