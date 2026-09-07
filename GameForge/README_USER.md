# GameForge - Universal Game Performance Optimizer

## Quick Start

### Option 1: Run Directly (Python required)
```
pip install psutil
python main.py
```

### Option 2: Build Executable (No Python needed)
```
build.bat
```
Then run `release\GameForge.exe`

## Commands

| Command | Description |
|---------|-------------|
| `GameForge.exe` | Full scan + diagnose + optimize |
| `GameForge.exe scan` | Scan hardware and games only |
| `GameForge.exe diagnose` | Diagnose stutter issues |
| `GameForge.exe optimize` | Apply all optimizations |
| `GameForge.exe cleanup` | Revert all changes |

## What It Does

1. **Scans** your hardware (CPU, GPU, RAM, Storage)
2. **Detects** installed games across Steam, Epic, GOG
3. **Diagnoses** why your games stutter
4. **Fixes** settings automatically
5. **Verifies** improvements
6. **Reverts** everything when done

## Requirements

- Windows 10/11 (64-bit)
- Python 3.9+ (for direct run)
- Administrator privileges (for system tweaks)
