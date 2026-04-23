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

I recommend installing `pipx` as well to run the CLI tool.

```bash
brew install pipx
```

## Install

Requires Python 3.13+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
```

```bash
uv build
```

```bash
pipx install dist/vid_split_to_x_py-0.1.0-py3-none-any.whl
```

If everything is set up correctly, you should now be able to run:

```bash
vid-split-to-x --help
```

## Usage

```
vid-split-to-x [OPTIONS] DIRECTORY
```

Scans `DIRECTORY` for `.mp4`, `.mov`, `.avi`, and `.mkv` files and splits any that exceed the size limit.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `-s`, `--size` | `3.9` | Max chunk size in GB |
| `-d`, `--delete` | off | Delete original file after splitting |
| `-t`, `--target` | — | Target directory to copy all output videos to |

**Examples:**

```bash
# Split videos over 3.9 GB in place
vid-split-to-x ~/Videos

# Custom 2 GB limit, delete originals after splitting
vid-split-to-x ~/Videos -s 2.0 -d

# Split and copy all output to a target directory
vid-split-to-x ~/Videos -t ~/Uploads

# Custom size limit with a target directory
vid-split-to-x ~/Videos -s 2.0 -t ~/Uploads
```

By default, output files are saved alongside the source video, named `{original_name}_{part}.{ext}` (e.g. `myvideo_1.mp4`, `myvideo_2.mp4`).

When `-t`/`--target` is specified:
- Videos that did not need splitting are copied to the target directory (never deleted from source).
- Videos that were split have their snippets moved to the target directory.
- If `-d` is also set, the original source file is deleted after splitting; otherwise it is left in place.

When `-d` is set without `-t`:
- Original files are deleted from the source directory after splitting.
- Videos that did not need splitting are left untouched.
