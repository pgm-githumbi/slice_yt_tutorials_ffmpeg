import re
import shutil
import os
import subprocess


def sanitize_filename(text):
    """Sanitizes a string to make it a valid filename."""
    return re.sub(r'[\\/:\*\?"<>|]', '_', text)


def extract_timestamp(time_str):
    """Extracts a timestamp in the format HH:MM:SS from a string."""
    match = re.search(r"(\d{2}):(\d{2}):(\d{2})", time_str)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return None


def extract_video_name_timestamp(timestamp_line):
    timestamp = extract_timestamp(timestamp_line)
    remaining_text = timestamp_line.replace(
        timestamp, "").strip() if timestamp else None
    print(f"\ntimestamp for {timestamp_line} is {timestamp}")
    print(f"remaining_text for {timestamp_line} is {remaining_text}\n")
    return timestamp, remaining_text


def delete_directory(directory_path):
    """Deletes a directory and its contents if it exists."""
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print("deleted directory", directory_path)
        return
    print("directory not found", directory_path)


def convert_to_seconds(time_str):
    """Converts a time string in HH:MM:SS format to seconds."""
    hours, minutes, seconds = map(int, time_str.split(":"))
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds


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


def in_powershell(command):
    pwrshell = ["powershell", "-NoProfile",
                "-ExecutionPolicy", "Bypass", "-Command",]
    if type(command) is list:
        return [*pwrshell, *command]
    return [*pwrshell, command]
