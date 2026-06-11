# yt-dlp: AI Quick Reference Guide

**Purpose**: Fast navigation and understanding of the yt-dlp codebase without reading all 5,000+ files.

---

## Project Overview

**yt-dlp** is a command-line video/audio downloader supporting 1,053+ sites with:
- Feature-rich extraction from video platforms (YouTube, Twitch, TikTok, etc.)
- Multiple download protocols (HTTP, HLS, DASH, RTMP, etc.)
- Post-processing (format conversion, audio extraction, muxing via FFmpeg)
- Extensible plugin architecture for custom extractors and post-processors
- Robust error handling and multiple network backends for reliability

**Key Facts**:
- **Language**: Python 3.10+
- **License**: The Unlicense (public domain)
- **Architecture**: Modular, layered design with ~1,053 site-specific extractors
- **Maintenance**: Active development, ~20k commits
- **Use Cases**: Personal video archival, streaming research, batch downloads

---

## Architecture at a Glance

yt-dlp follows a **4-layer architecture**:

```
User (CLI) or Library
     ↓
[1] ORCHESTRATION (YoutubeDL.py)
     ├─ Parses options, selects extractor, manages download flow
     ↓
[2] EXTRACTION (extractor/)
     ├─ Site-specific extractors parse HTML/APIs for metadata
     ├─ Returns: {id, title, url, duration, formats, ...}
     ↓
[3] DOWNLOADING (downloader/)
     ├─ Protocol-specific: HTTP, HLS, DASH, RTMP, fragment-based, external
     ├─ Handles fragmentation, streaming, retries
     ↓
[4] POST-PROCESSING (postprocessor/)
     ├─ Format conversion, muxing, metadata embedding
     ├─ Audio extraction, sponsorship removal, etc.
     ↓
Output File
```

Each layer is **independent**—new protocols, extractors, or processors can be added without touching other layers.

---

## Directory Structure Map

```
yt_dlp/
├── YoutubeDL.py              # [1] Main orchestrator (4,512 lines)
├── __init__.py               # [1] CLI entry point & main()
├── options.py                # [1] Argument parser (2,009 lines)
├── globals.py                # Config and state management
├── version.py                # Version info
│
├── extractor/                # [2] EXTRACTION LAYER
│   ├── __init__.py           # Extractor registry & gen_extractor_classes()
│   ├── common.py             # InfoExtractor base class (~2,000 lines)
│   ├── generic.py            # Fallback generic extractor
│   ├── _extractors.py        # Auto-generated registry (54,810 lines)
│   ├── youtube/              # YouTube sub-package (modular)
│   │   ├── __init__.py
│   │   ├── _base.py          # YoutubeBaseInfoExtractor
│   │   ├── _video.py         # YoutubeIE (videos)
│   │   ├── _tab.py           # YoutubeTabIE (playlists)
│   │   ├── _search.py        # Search functionality
│   │   ├── jsc/              # JavaScript player logic
│   │   └── pot/              # Player Other Transcripts
│   ├── abc.py, abcnews.py, ... # 1,050+ individual extractors
│
├── downloader/               # [3] DOWNLOADING LAYER
│   ├── common.py             # BaseDownloader class
│   ├── http.py               # HTTP/HTTPS downloads
│   ├── hls.py                # HTTP Live Streaming (M3U8)
│   ├── dash.py               # DASH streaming
│   ├── fragment.py           # Fragment-based downloads
│   ├── external.py           # External tools (curl, aria2, etc.)
│   ├── f4m.py, ism.py, mhtml.py, rtmp.py, ... # Protocol support
│
├── postprocessor/            # [4] POST-PROCESSING LAYER
│   ├── common.py             # BasePostProcessor class
│   ├── ffmpeg.py             # FFmpeg wrapper (48,251 lines)
│   ├── embedthumbnail.py     # Thumbnail embedding
│   ├── sponsorblock.py       # Sponsorship removal
│   ├── modify_chapters.py    # Chapter modification
│
├── networking/               # Network request handling
│   ├── common.py             # RequestHandler base
│   ├── _urllib.py, _requests.py, _curlcffi.py # Multiple backends
│   ├── impersonate.py        # Browser impersonation
│
├── utils/                    # Utility functions
│   ├── _utils.py             # 5,728 lines of helpers (HUGE)
│   ├── traversal.py          # Path traversal utilities
│   ├── _jsruntime.py         # JavaScript runtime wrappers
│   ├── networking.py         # Network helpers
│   ├── jslib/                # JavaScript libraries
│
├── compat/                   # Python version compatibility
└── dependencies/             # External dependency management

test/                         # TEST SUITE
├── test_*.py                 # 37+ test files
├── conftest.py               # pytest configuration & fixtures
├── helper.py                 # Test utilities (13,938 lines)
├── testdata/                 # Fixtures and test data

Makefile                      # Build targets (make test, make lazy-extractors, etc.)
pyproject.toml                # Build config, dependencies, entry points
CONTRIBUTING.md               # Contribution guidelines
README.md                      # Full documentation (178 KB)
supportedsites.md             # List of 1,053 supported sites
```

---

## Entry Points & Key Classes

### CLI Entry
```bash
# Runs: yt_dlp/__init__.py::main()
python3 -m yt_dlp https://youtube.com/watch?v=dQw4w9WgXcQ
```

**Flow**:
1. `yt_dlp/__init__.py::main()` → parses CLI arguments via `options.py`
2. Creates `YoutubeDL` instance with options dict
3. Calls `YoutubeDL.download([urls])`
4. Returns exit code

### Library Entry
```python
# Use as Python library
from yt_dlp import YoutubeDL

ydl = YoutubeDL({'format': 'best', 'outtmpl': '%(title)s.%(ext)s'})
ydl.download(['https://youtube.com/watch?v=dQw4w9WgXcQ'])
```

### Core Classes

| Class | File | Purpose |
|-------|------|---------|
| `YoutubeDL` | `YoutubeDL.py` | Orchestrator: format selection, download flow, post-processing |
| `InfoExtractor` | `extractor/common.py` | Base for all 1,053 extractors; helper methods for HTML/JSON parsing |
| `BaseDownloader` | `downloader/common.py` | Base for protocol-specific downloaders |
| `BasePostProcessor` | `postprocessor/common.py` | Base for post-processors (FFmpeg, muxing, etc.) |
| `RequestHandler` | `networking/common.py` | Abstract HTTP request handler; multiple backends supported |

### Metadata Structure
All extractors return a dict:
```python
{
    'id': 'video_id',
    'title': 'Video Title',
    'url': 'http://example.com/video.mp4',  # or 'formats' list
    'formats': [  # List of available formats
        {
            'format_id': '22',
            'ext': 'mp4',
            'format': '720p',
            'url': 'http://...',
            'height': 720,
            'fps': 30,
            ...
        },
        ...
    ],
    'duration': 180,
    'uploader': 'Channel Name',
    'upload_date': '20240101',
    'ext': 'mp4',
    # ... many optional fields
}
```

---

## Common Patterns & Conventions

### Extractor Pattern
Every extractor inherits from `InfoExtractor` and implements:

```python
class SiteNameIE(InfoExtractor):
    _VALID_URL = r'https://site\.com/video/(?P<id>[^/?#&]+)'
    IE_NAME = 'sitename'
    _TESTS = [...]  # Test cases
    
    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        title = self._search_regex(r'<h1>(.+?)</h1>', webpage, 'title')
        
        return {
            'id': video_id,
            'title': title,
            'formats': [...],  # or 'url'
            'duration': int_or_none(...),
        }
```

**Helper Methods** (from `InfoExtractor`):
- `self._download_webpage(url, video_id)` — Fetch HTML
- `self._download_json(url, video_id)` — Fetch and parse JSON
- `self._search_regex(pattern, text, group_name)` — Regex extraction
- `self._match_id(url)` — Extract ID from URL via `_VALID_URL`

### Plugin Architecture
Plugins extend functionality via custom extractors, post-processors, or downloaders.

**Plugin Location**: `~/.yt-dlp/plugins/` (or `yt-dlp/plugins/` in portable mode)

**Plugin Naming**:
- Extractors: `*IE` suffix (e.g., `MyCustomSiteIE`)
- Post-processors: `*PP` suffix (e.g., `MyCustomPP`)
- Downloaders: `*D` suffix (e.g., `MyProtoD`)

**Registration**: Plugins are auto-discovered and registered via `PluginSpec` in `globals.py`.

### Lazy Loading
Importing all 1,053 extractors at startup is slow. Solution:

```bash
# Build lazy loader (imports on first use)
make lazy-extractors
```

This generates `yt_dlp/extractor/lazy_extractors.py`, which:
- Caches all extractor imports
- Speeds up CLI startup from ~2s → ~0.3s
- **Must be rebuilt** when adding a new extractor

### Error Handling
```python
from yt_dlp.utils import ExtractorError, DownloadError

# In extractors
raise ExtractorError('Video not found', expected=True)  # User's fault

# In downloaders
raise DownloadError('Network timeout')  # System/network issue
```

Base exception: `YoutubeDLError` (catches all)

### Configuration Priority
1. CLI arguments (highest priority)
2. Config files: `~/.yt-dlp/config.txt`, portable dir config
3. Environment variables: `YDL_*` prefix
4. Hardcoded defaults in code (lowest priority)

### Testing
- **Framework**: pytest
- **Run offline tests**: `make offlinetest`
- **Run all tests**: `make test` (includes network tests)
- **Test markers**:
  ```python
  @pytest.mark.download  # Requires network
  @pytest.mark.skip  # Skipped
  ```
- **Fixtures** (from `conftest.py`):
  - `handler` — Parametrizes across request handlers (urllib, requests, curl-cffi)
  - `skip_handler` — Skip test for specific handlers

### Code Quality
Required before commit:
- `ruff check .` — Linting (line length, imports, etc.)
- `autopep8 --diff .` — PEP 8 style
- Pre-commit hooks enforce this (`.pre-commit-config.yaml`)

---

## Critical File Index

| File | Lines | Purpose |
|------|-------|---------|
| `YoutubeDL.py` | 4,512 | Core orchestrator: format selection, download flow, error handling |
| `__init__.py` | 1,113 | CLI entry point, `main()` function |
| `options.py` | 2,009 | All CLI option definitions |
| `extractor/common.py` | ~2,000 | `InfoExtractor` base class, helper methods |
| `extractor/__init__.py` | 55 | Extractor registry, `gen_extractor_classes()` |
| `extractor/youtube/_base.py` | ~1,500 | YouTube-specific base (signature extraction, n-param handling) |
| `downloader/common.py` | 20,700 | `BaseDownloader`, retry logic, progress reporting |
| `downloader/http.py` | 16,515 | HTTP/HTTPS downloads with ranges, resume, etc. |
| `downloader/hls.py` | 19,559 | HLS/M3U8 stream downloading |
| `downloader/external.py` | 28,916 | Delegates to curl, aria2, ffmpeg, etc. |
| `postprocessor/ffmpeg.py` | 48,251 | FFmpeg wrapper for muxing, conversion, audio extraction |
| `utils/_utils.py` | 5,728 | 100+ utility functions (parsing, regex, formatting) |
| `networking/common.py` | 608 | `RequestHandler` base, proxy support, headers |
| `test/conftest.py` | 200+ | pytest fixtures and parametrization |
| `pyproject.toml` | 300+ | Dependencies, build config, entry points |

---

## Common Tasks

### Add a New Extractor for a Video Site

1. **Create file**: `yt_dlp/extractor/mynewsite.py`
   ```python
   from .common import InfoExtractor
   
   class MyNewsiteIE(InfoExtractor):
       IE_NAME = 'mynewsite'
       _VALID_URL = r'https://mynewsite\.com/(?:video|watch)/(?P<id>[^/?#]+)'
       
       def _real_extract(self, url):
           video_id = self._match_id(url)
           webpage = self._download_webpage(url, video_id)
           
           title = self._search_regex(r'<h1>(.+?)</h1>', webpage, 'title')
           video_url = self._search_regex(r'src="([^"]+\.mp4)"', webpage, 'video')
           
           return {
               'id': video_id,
               'title': title,
               'url': video_url,
               'ext': 'mp4',
           }
   ```

2. **Test it**: `pytest test/test_download.py::TestExtractors::test_MyNewsiteIE -xvs`

3. **Rebuild lazy loader**: `make lazy-extractors` (required for CLI)

4. **Add tests**: Create `_TESTS` in the class with sample URLs

### Fix a Broken Extractor

1. **Identify the issue**: Run with verbose flag
   ```bash
   python3 -m yt_dlp -vU https://site.com/video/123
   ```
   Look for HTML structure changes, API responses, or signature extraction failures

2. **Update extraction logic**: Modify `_real_extract()` to match new HTML/API

3. **Test**: `pytest test/test_download.py::TestExtractors::test_SiteIE -xvs`

4. **Commit with PR**: Reference the issue/pull request number

### Run Tests

```bash
# Offline tests only (fast, no network)
make offlinetest

# All tests including network (slow)
make test

# Specific test file
pytest test/test_utils.py -xvs

# Specific test class/function
pytest test/test_YoutubeDL.py::TestYoutubeDL::test_format_selection -xvs

# With coverage
pytest --cov=yt_dlp test/
```

### Debug Extraction Failure

```bash
# Verbose output
python3 -m yt_dlp -vU https://site.com/video/123

# Save webpage for inspection
python3 -m yt_dlp --write-debug-json https://site.com/video/123

# Check what extractor is used
python3 -m yt_dlp --print-to-file "%(ie_key)s" -o "IE.txt" https://site.com/video/123
```

### Build and Distribute

```bash
# Generate lazy extractors (required)
make lazy-extractors

# Build source distribution
python3 -m build

# Install locally
pip install -e ".[default]"

# Generate shell completions
make completions
```

---

## Key Dependencies & Why

| Dependency | Version | Purpose |
|------------|---------|---------|
| **requests** | ≥2.32.2 | HTTP client (primary backend) |
| **brotli** / **brotlicffi** | Latest | HTTP compression (br encoding) |
| **urllib3** | Latest | Low-level HTTP, connection pooling |
| **websockets** | ≥13.0 | WebSocket support (some live streams) |
| **yt-dlp-ejs** | ==0.8.0 | JavaScript execution for player (YouTube, etc.) |
| **pycryptodomex** | Latest | AES encryption for DRM-free streams |
| **certifi** | Latest | SSL/TLS root certificates |
| **mutagen** | Latest | Audio metadata (ID3, etc.) |

**Optional**:
- **curl-cffi** — curl backend with browser impersonation (evades blocks)
- **deno** — Alternative JS runtime (faster than yt-dlp-ejs)
- **secretstorage** — Linux keyring for cookie storage

---

## Module Import Patterns

### As CLI Tool
```bash
python3 -m yt_dlp [options] [URLs]
```

### As Library
```python
from yt_dlp import YoutubeDL

ydl_opts = {
    'format': 'best[ext=mp4]',
    'outtmpl': '%(title)s.%(ext)s',
    'progress_hooks': [my_progress_hook],
}

with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('https://youtube.com/watch?v=...', download=False)
    print(info['title'])
```

### Plugin Discovery
```python
from yt_dlp.utils import get_plugins  # Load all registered plugins

plugins = get_plugins()
for spec in plugins.get('ie', []):  # 'ie' = extractors
    print(spec.module_name, spec.class_name)
```

### Lazy Loader (Auto-generated)
```python
from yt_dlp.extractor import gen_extractor_classes

# First call is slow (imports all 1,053), subsequent calls are instant
extractors = gen_extractor_classes()
for ie_class in extractors:
    print(ie_class.IE_NAME)
```

---

## Development Workflow

### Setup
```bash
git clone https://github.com/yt-dlp/yt-dlp
cd yt-dlp
python3 -m pip install -e ".[default]"
```

### Before Each Commit
```bash
# Run offline tests
make offlinetest

# Or check code quality manually
ruff check .
autopep8 --diff .
pytest test/test_YoutubeDL.py -xvs
```

### Adding a New Extractor (Full Workflow)
1. Create extractor file in `yt_dlp/extractor/`
2. Implement `_VALID_URL`, `IE_NAME`, `_real_extract()`
3. Add test cases in `_TESTS`
4. Run: `make lazy-extractors`
5. Test: `pytest test/test_download.py -k YourSiteIE -xvs`
6. Commit with message: `[ie/sitename] Add new extractor`

### Debugging Network Issues
```bash
# Use curl-cffi backend (better for blocked sites)
pip install curl-cffi
python3 -m yt_dlp --http-chunks 1 \
  --external-downloader curl_cffi \
  --http-no-ssl-cert-verify \  # Only if necessary
  https://site.com/video/123
```

### Profiling Performance
```bash
# Time extractor
time python3 -m yt_dlp -F https://site.com/video/123

# Profile memory
python3 -m memory_profiler -m yt_dlp https://site.com/video/123

# Profile CPU
python3 -m cProfile -s cumtime -m yt_dlp https://site.com/video/123 | head -20
```

---

## Quick Navigation Summary

**Need to understand...** → **Check file(s)**

- **How downloads are orchestrated** → `YoutubeDL.py`
- **How to add a new extractor** → `extractor/common.py` (base class) + example in `extractor/youtube/_video.py`
- **How to add a new download protocol** → `downloader/common.py` (inherit `BaseDownloader`)
- **How post-processing works** → `postprocessor/ffmpeg.py` (most complex example)
- **All available CLI options** → `options.py`
- **How plugins work** → `globals.py` + `plugins.py`
- **Testing patterns** → `test/conftest.py` + `test/test_download.py`
- **Utility functions** → `utils/_utils.py` (search here first)
- **A specific extractor** → `extractor/{sitename}.py` or `extractor/{sitename}/_variant.py`

---

**Last Updated**: 2026-04-26  
**For Latest**: See `README.md`, `CONTRIBUTING.md`, or GitHub issues
