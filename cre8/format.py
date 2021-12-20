import math
from datetime import timedelta


def format_timer(remaining_duration: timedelta):
    remaining_secs = remaining_duration.total_seconds()
    hours = int(remaining_secs // 3600)
    remaining_secs -= (hours * 3600)
    mins = int(remaining_secs // 60)
    remaining_secs -= (mins * 60)
    secs = math.floor(remaining_secs)
    if hours > 0:
        text = '{:d}h{:d}m{:d}s'.format(hours, mins, secs)
    elif mins > 0:
        text = '{:d}m{:d}s'.format(mins, secs)
    else:
        text = '{:d}s'.format(secs)
        
    return text
    
    
def pad_left(width: int, text: str, pad_char: str = ' ') -> str:
    """
    Add spacing before text to reach the desired length.
    
    :param width: The desired length. If length of text already meets this, no padding is added.
    :param text: The text to insert padding before.
    :param pad_char: The character to insert to meet desired width.
    :return: The left-padded text.
    """
    space_needed = max(width - len(text), 0)
    return (pad_char * space_needed) + text
    
    
def pad_right(width: int, text: str, pad_char: str = ' ') -> str:
    """
    Add spacing after text to reach the desired length.
    
    :param width: The desired length. If length of text already meets this, no padding is added.
    :param text: The text to insert padding after.
    :param pad_char: The character to insert to meet desired width.
    :return: The right-padded text.
    """
    space_needed = max(width - len(text), 0)
    return text + (pad_char * space_needed)
    
    
def pad_middle(width: int, left: str, right: str, pad_char: str = ' ') -> str:
    """
    Add spacing between left and right strings to reach the desired length. Will always
    insert at least one space of padding even if it would exceed width.
    
    :param width: The desired length. If total length of left + right already exceeds
    this, only one space of padding is inserted.
    :param left: The text on the left.
    :param right: The text on the right.
    :param pad_char: The character to insert to meet desired width.
    :return: The middle-padded text.
    """
    text_len = len(left) + len(right)
    space_needed = max(width - text_len, 1)
    text = left + (pad_char * space_needed) + right
    return text
