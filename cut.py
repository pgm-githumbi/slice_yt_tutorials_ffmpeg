import os
import re
import subprocess
from typing import Any

from utils import convert_to_seconds, extract_timestamp, sanitize_filename


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

cmds = [f"mkdir \"{long_video_name}\"",
        f"cd \"{long_video_name}\"",
        f"pwd",
        f"ffmpeg -ss 00:00:00 -i \"{long_video}\" -t 180 -c copy \"{long_video_name}\{long_video_name}_out.mp4\""]
print(f"\n\n{cmds}")
# for cmd in cmds:
#     completed = subprocess.run(cmd, shell=True, capture_output=True)
#     print("\n\nreturns", completed.returncode)
#     print("\n\nstdout", completed.stdout)
#     print("\n\nstderr", completed.stderr)


def extract_video_name_timestamp(timestamp_line):
    timestamp = extract_timestamp(timestamp_line)
    remaining_text = timestamp_line.replace(
        timestamp, "").strip() if timestamp else None
    return timestamp, remaining_text


def in_powershell(command):
    pwrshell = ["powershell", "-NoProfile",
                "-ExecutionPolicy", "Bypass", "-Command",]
    if type(command) is list:
        return [*pwrshell, *command]
    return [*pwrshell, command]


def get_video_length_in_seconds(video_path):
    """Gets the length of a video in seconds using ffprobe."""
    try:
        result = subprocess.run(
            in_powershell(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                           "-of", "default=noprint_wrappers=1:nokey=1", f"\"{video_path}\""]),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            duration = float(result.stdout)
            return duration
        else:
            print(f"Error getting video length: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error getting video length: {e}")
        return None


long_video_len = get_video_length_in_seconds(long_video)
subprocess.run(f"mkdir \"{long_video_name}\"", shell=True,
               stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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

    if timestamp:
        short_vid_len_secs = next_timestamp_secs - timestamp_secs
        command = f"ffmpeg -ss {timestamp} -i \"{long_video}\" -t {short_vid_len_secs} -c copy \"{long_video_name}\{i} - {vid_name}.mp4\""
        print("command: ", command, "\n\n================================")
        if short_vid_len_secs > 0:
            subprocess.run(command, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, shell=True)
