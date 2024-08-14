import re


def sanitize_filename(text):
    """Sanitizes a string to make it a valid filename."""
    return re.sub(r'[\\/:\*\?"<>|]', '_', text)


def extract_timestamp(time_str):
    """Extracts a timestamp in the format HH:MM:SS from a string."""
    match = re.search(r"(\d{2}):(\d{2}):(\d{2})", time_str)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return None


def convert_to_seconds(time_str):
    """Converts a time string in HH:MM:SS format to seconds."""
    hours, minutes, seconds = map(int, time_str.split(":"))
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds
