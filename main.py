import subprocess
import os
import sys

def split_video_by_size(video_path, *, output_dir=".", max_size_gb=3.9):
    max_size_bytes = max_size_gb * 1024**3 # multiply max size gb by bytes per gb
    file_size = os.path.getsize(video_path) # get video file size

    if file_size <= max_size_bytes:
        return
    
    num_parts = int(-(-file_size // max_size_bytes)) # ceiling division to get num of parts to split video to
    print(num_parts)
    # get the duration of the video
    get_duration_result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1:nokey=1', video_path],
         capture_output=True, text=True
    )
    duration = float(get_duration_result.stdout)
    print(duration)

    segment_duration = duration / num_parts

    base_name, extension = os.path.splitext(os.path.basename(video_path))

    for i in range(num_parts):
        start_time = i * segment_duration
        output_file = f"{output_dir}/{base_name}_{i+1}{extension}"        

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_time),
            '-t', str(segment_duration),
            '-c:v', 'copy', # copy video codec 
            '-c:a', 'copy', # copy audio codec
            output_file
        ]

        print(f"Creating part {i+1}/{num_parts}...")
        split_video_result = subprocess.run(cmd, capture_output=True)  # noqa: F841

        part_size = os.path.getsize(output_file) / 1024**3
        print(f"Part {i+1} size: {part_size:.2f} GB")
    
    print(f"Done processing video {base_name}{extension}")

def get_videos_from_dir(dir_path):
    videos = [video for video in os.listdir(dir_path) if os.path.splitext(os.path.basename(video))[1].lower() in ['.mp4', '.mov']]
    return videos

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <directory path> <max size (GB)> <optional: delete original (True/False)>")
        return

    dir_path = sys.argv[1]
    max_size_gb = float(sys.argv[2])
    delete_original = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False
    videos = get_videos_from_dir(dir_path)
    print(f"Found {len(videos)} videos in directory '{dir_path}':")
    for video in videos:
        if os.path.getsize(os.path.join(dir_path, video)) > max_size_gb * 1024**3:
            print(f"Splitting video: {video}")
            split_video_by_size(os.path.join(dir_path, video), output_dir=dir_path, max_size_gb=max_size_gb)
        else:
            print(f"Video '{video}' is smaller than {max_size_gb} GB, skipping split.")
        if delete_original:
            os.remove(os.path.join(dir_path, video))
            print(f"Deleted original video: {video}")

if __name__ == "__main__":
    main()