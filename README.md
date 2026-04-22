# vid-split-to-x

Split large video files into chunks under a target file size (default: 3.9 GB).

## Prerequisites

**ffmpeg** must be installed and on your `PATH`:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## Install

Requires Python 3.13+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

```
vid-split-to-x [OPTIONS] DIRECTORY
```

Scans `DIRECTORY` for `.mp4` and `.mov` files and splits any that exceed the size limit.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `-s`, `--size` | `3.9` | Max chunk size in GB |
| `-d`, `--delete` | off | Delete original file after splitting |

**Examples:**

```bash
# Split videos over 3.9 GB
vid-split-to-x ~/Videos

# Custom 2 GB limit, delete originals after splitting
vid-split-to-x ~/Videos -s 2.0 -d
```

Output files are saved alongside the source video, named `{original_name}_{part}.{ext}` (e.g. `myvideo_1.mp4`, `myvideo_2.mp4`).
