import subprocess
import os
import shutil
import click

def split_video_by_size(video_path, num_parts, *, output_dir=".", max_size_gb=3.9):
    if num_parts <= 1:
        return []

    get_duration_result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1:nokey=1', video_path],
         capture_output=True, text=True
    )
    duration = float(get_duration_result.stdout)

    segment_duration = duration / num_parts

    base_name, extension = os.path.splitext(os.path.basename(video_path))

    output_files = []
    for i in range(num_parts):
        start_time = i * segment_duration
        output_file = os.path.join(output_dir, f"{base_name}_{i+1}{extension}")

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_time),
            '-t', str(segment_duration),
            '-c:v', 'copy', # copy video codec
            '-c:a', 'copy', # copy audio codec
            output_file
        ]

        subprocess.run(cmd, capture_output=True)
        output_files.append(output_file)

    return output_files

def get_videos_info(dir_path, max_size_gb):
    videos = [video for video in os.listdir(dir_path) if os.path.splitext(os.path.basename(video))[1].lower() in ['.mp4', '.mov', '.avi', '.mkv']]
    max_size_bytes = max_size_gb * 1024**3
    result = []
    for video in videos:
        video_path = os.path.join(dir_path, video)
        file_size = os.path.getsize(video_path)
        parts = int(-(-file_size // max_size_bytes)) if file_size > max_size_bytes else 1
        result.append((video_path, parts))
    return result

@click.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('-s', '--size', 'size', type=float, default=3.9, help='Maximum file size in GB (default: 3.9)')
@click.option('-d', '--delete', 'delete', is_flag=True, help='Delete original videos after splitting')
@click.option('-t', '--target', 'target', type=click.Path(), default=None, help='Target directory to move all output videos to')
def cli(directory, size, delete, target):
    """Split videos in directory to chunks of given size GB."""
    dir_path = directory
    max_size_gb = size
    delete_original = delete

    if target is not None:
        os.makedirs(target, exist_ok=True)

    videos_info = get_videos_info(dir_path, max_size_gb)

    click.echo(f"Found {len(videos_info)} videos in directory '{dir_path}'")

    total_parts = sum(parts for _, parts in videos_info)

    with click.progressbar(length=total_parts, label='Processing videos') as bar:
        for video_path, num_parts in videos_info:
            if num_parts > 1:
                snippet_paths = split_video_by_size(video_path, num_parts, output_dir=dir_path, max_size_gb=max_size_gb)
                if target is not None:
                    for snippet in snippet_paths:
                        shutil.move(snippet, os.path.join(target, os.path.basename(snippet)))
                if delete_original:
                    os.remove(video_path)
            else:
                # No split needed — copy to target if set, never delete
                if target is not None:
                    shutil.copy2(video_path, os.path.join(target, os.path.basename(video_path)))
            bar.update(num_parts)

    subprocess.run(["afplay", "/System/Library/Sounds/Frog.aiff"])

if __name__ == "__main__":
    cli()
