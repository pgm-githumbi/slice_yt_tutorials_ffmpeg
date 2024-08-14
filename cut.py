import os
import re
import subprocess
from typing import Any

from regex import F

from utils import convert_to_seconds, delete_directory, extract_timestamp, get_video_length_in_seconds, sanitize_filename


timestamps = """
(00:00:00) Lesson 0: Welcome To Blockchain
(00:09:05) Lesson 1: Blockchain Basics
(02:01:16) Lesson 2: Welcome to Remix! Simple Storage
(03:05:34) Lesson 3: Remix Storage Factory
(03:31:55) Lesson 4: Remix Fund Me
(05:30:42) Lesson 5: Ethers.js Simple Storage
(08:20:17) Lesson 6: Hardhat Simple Storage
(10:00:48) Lesson 7: Hardhat Fund Me
(12:32:57) Lesson 8: HTML / Javascript Fund Me (Full Stack / Front End)
(13:41:02) Lesson 9: Hardhat Smart Contract Lottery
(16:34:07) Lesson 10: NextJS Smart Contract Lottery (Full Stack / Front End)
(18:51:36) Lesson 11: Hardhat Starter Kit
(18:59:24) Lesson 12: Hardhat ERC20s
(19:16:13) Lesson 13: Hardhat DeFi & Aave
(20:28:51) Lesson 14: Hardhat NFTs 
(23:37:03) Lesson 15: NextJS NFT Marketplace (Full Stack / Front End)
(28:53:11) Lesson 16: Hardhat Upgrades
(29:45:24) Lesson 17: Hardhat DAOs
(31:28:32) Lesson 18: Security & Auditing 
 """

long_video = "D:\@Videos\-2024 March\Mia Khalifa Threesome BBC - EPORNER.mp4"
long_video_name = long_video.split(os.sep)[-1]
sections = timestamps.splitlines()


def extract_video_name_timestamp(timestamp_line):
    timestamp = extract_timestamp(timestamp_line)
    remaining_text = timestamp_line.replace(
        timestamp, "").strip() if timestamp else None
    return timestamp, remaining_text


os.chdir('temp')
print(os.getcwd())

long_video_len = get_video_length_in_seconds(long_video)
directory_name = f'{long_video_name}'
directory_name = os.path.join(os.getcwd(), directory_name)

try:
    delete_directory(directory_name)
except PermissionError:
    print("Could not delete directory")


os.makedirs(directory_name, exist_ok=True)


for i in range(len(sections)):
    section = sections[i]
    next_section = sections[i + 1] if i + 1 < len(sections) else None
    timestamp, vid_name = extract_video_name_timestamp(section)

    vid_name = sanitize_filename(vid_name) if vid_name else vid_name
    next_vid_time = extract_video_name_timestamp(
        next_section) if next_section else None, None

    ((next_timestamp, next_vid_name),
     _) = next_vid_time if next_vid_time else ((None, None), None)

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
                      '-i', long_video, '-t', f'{short_vid_len_secs}', '-c', 'copy',
                      output]
        print("command: ", ffmpeg_cmd)
        if short_vid_len_secs > 0:
            result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, shell=True)
            print("\n", result)
    print("\n\n================================")
