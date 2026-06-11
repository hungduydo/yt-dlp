# yt-dlp Standalone Executable - Distribution Guide

## What You Have

**File**: `yt-dlp_macos_arm64.tar.gz` (25 MB)

A standalone executable for macOS arm64 (Apple Silicon / M1/M2/M3+) that includes:
- yt-dlp with all 1,000+ video extractors
- All required dependencies (requests, brotli, certifi, websockets, etc.)
- No Python installation needed
- Pre-configured with Bilibili HTTP 412 fix

## Installation

### Method 1: Extract and Run
```bash
# Extract the archive
tar -xzf yt-dlp_macos_arm64.tar.gz

# Make it executable (usually done automatically)
chmod +x yt-dlp

# Run it
./yt-dlp --version
./yt-dlp https://www.bilibili.com/video/BV1uK4y1v7B2/
```

### Method 2: Install to System PATH
```bash
# Extract to /usr/local/bin (requires sudo)
sudo tar -xzf yt-dlp_macos_arm64.tar.gz -C /usr/local/bin

# Now use it from anywhere
yt-dlp --version
```

## Basic Usage Examples

### Download a video
```bash
./yt-dlp https://www.bilibili.com/video/BV1uK4y1v7B2/
```

### List available formats
```bash
./yt-dlp -F https://www.bilibili.com/video/BV1uK4y1v7B2/
```

### Download specific quality
```bash
./yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" https://example.com/video
```

### Download entire playlist
```bash
./yt-dlp https://www.youtube.com/playlist?list=EXAMPLE
```

### Download with subtitles
```bash
./yt-dlp --write-subs --sub-lang en https://example.com/video
```

### Extract audio only (MP3)
```bash
./yt-dlp -f "ba" -x --audio-format mp3 https://example.com/video
```

## System Requirements

- **macOS 10.13** or later
- **Apple Silicon** (M1, M2, M3, M4, etc.) - this build is arm64 only
- **~25 MB** disk space for the executable
- Internet connection for downloads
- **No Python installation needed!**

## Features Included

✅ Video downloads from 1,000+ sites including:
- YouTube, Bilibili, TikTok, Instagram, Twitch, etc.

✅ Format selection and quality control

✅ Playlist support

✅ Subtitle/caption downloading

✅ Audio extraction (MP3, WAV, etc.)

✅ Video conversion (with FFmpeg installed)

✅ Proxy support

✅ Cookie-based authentication

## Troubleshooting

### "Permission denied" error
```bash
chmod +x yt-dlp
./yt-dlp --help
```

### "Cannot open" on macOS
If you get "cannot be opened because it is from an unidentified developer":
1. First attempt to run it: `./yt-dlp --version`
2. Go to System Preferences → Security & Privacy
3. Click "Open Anyway" next to the yt-dlp warning

### HTTP 412 errors are fixed
This build includes the fix for Bilibili's HTTP 412 Precondition Failed errors. If you were having issues downloading from Bilibili, they should now be resolved.

### Need FFmpeg for video conversion?
```bash
# Install FFmpeg for video format conversion
brew install ffmpeg

# Then use yt-dlp to convert videos
./yt-dlp -f "best" --recode-video mp4 https://example.com/video
```

## Updating

To update to a newer version:
```bash
./yt-dlp -U
```

Or download the latest release from the GitHub releases page.

## Configuration

Create `~/.config/yt-dlp/config.txt` for persistent settings:
```
# Example config file
--output "%(title)s [%(id)s].%(ext)s"
--restrict-filenames
--prefer-free-formats
--no-playlist
```

## Support & Documentation

- **Help**: `./yt-dlp --help`
- **Supported Sites**: `./yt-dlp --list-extractors`
- **GitHub**: https://github.com/yt-dlp/yt-dlp
- **Wiki**: https://github.com/yt-dlp/yt-dlp/wiki

## Build Information

- **Built**: April 26, 2026
- **Version**: 2026.03.17
- **Platform**: macOS arm64 (Apple Silicon)
- **Build Tool**: PyInstaller 6.20.0
- **Includes Bilibili Fix**: Yes ✅

## License

yt-dlp is released under the Unlicense (public domain). You can use it freely for any purpose.

---

**Note**: This is a compiled executable for Apple Silicon Macs. For Intel Macs or Windows/Linux, you'll need to build your own or find other distribution methods.
