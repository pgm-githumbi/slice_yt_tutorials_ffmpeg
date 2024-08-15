import argparse
import os
import re
import subprocess
from typing import Any

from regex import F

from utils import convert_to_seconds, delete_directory, extract_timestamp, extract_video_name_timestamp, get_video_length_in_seconds, sanitize_filename


output_directory = os.getcwd()


def process_file_in_pairs(filename):
    """Processes file lines in pairs.

    Args:
      filename: The path to the file.

    Yields:
      Tuples of two consecutive lines or a single line if the file has an odd number of lines.
    """

    with open(filename, 'r') as file:
        lines = iter(file)
        prev_line2 = next(lines)
        while True:
            try:
                line1 = prev_line2
                line2 = next(lines)
                yield line1.strip(), line2.strip()
                prev_line2 = line2
            except StopIteration:
                # If we reach the end of the file and there's an odd number of lines
                if line1:
                    yield line1.strip(), None
                break


parser = argparse.ArgumentParser(
    description="cut yt tutorial into segments based on a timestamps text file.")
parser.add_argument("--input_file", type=str, required=True,
                    help="Path to the video file to be cut into segments")
parser.add_argument("--timestamps", required=True, type=str, help=""".txt file containing newline separate 
                    strings containing HH:MM:SS timestamps and a title for each video.
                    The input-file will be split into the number of lines with a valid timestamp
                    in this file (if enough video is available)""")
parser.add_argument("--output_folder", type=str, default=output_directory,
                    help="Where to put the cut up videos.")

args = parser.parse_args()
output_directory = args.output_folder

os.makedirs(output_directory, exist_ok=True)
os.chdir(output_directory)

long_video_len = get_video_length_in_seconds(args.input_file)
long_video_name = args.input_file.split(os.sep)[-1]
directory_name = f'{long_video_name}'
directory_name = os.path.join(os.getcwd(), directory_name)

try:
    delete_directory(directory_name)
except PermissionError:
    print("Could not delete directory")


os.makedirs(directory_name, exist_ok=True)


for i, (line, next_line) in enumerate(process_file_in_pairs(args.timestamps)):
    timestamp, vid_name = extract_video_name_timestamp(line)

    vid_name = sanitize_filename(vid_name) if vid_name else vid_name
    next_vid_time = extract_video_name_timestamp(
        next_line) if next_line else None, None

    if next_vid_time and next_vid_time[0]:
        ((next_timestamp, next_vid_name), _) = next_vid_time
    else:
        next_timestamp, next_vid_name = None, None

    timestamp_secs = convert_to_seconds(timestamp) if timestamp else None
    if timestamp_secs and timestamp_secs > long_video_len:
        break

    next_timestamp_secs = convert_to_seconds(
        next_timestamp) if next_timestamp else long_video_len

    output_folder = f"{long_video_name}"
    output_folder = sanitize_filename(output_folder)
    output_file = f"{i} - {vid_name}.mp4"
    output_file = sanitize_filename(output_file)
    output = os.path.join(os.getcwd(), output_folder, output_file)

    if timestamp:
        short_vid_len_secs = min(
            long_video_len, next_timestamp_secs) - timestamp_secs
        ffmpeg_cmd = ['ffmpeg', '-loglevel', 'error', '-ss', f'{timestamp}',
                      '-i', args.input_file, '-t', f'{short_vid_len_secs}', '-c', 'copy',
                      output]
        if short_vid_len_secs > 0:
            result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, shell=True)
    print("\n\n================================")
