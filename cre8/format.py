import math
from datetime import timedelta

from typing import Tuple

# power of 10, abbreiviation, full
NumberNames = [
    (6, 'M', 'million'),
    (9, 'B', 'billion'),
    (12, 'T', 'trillion'),
    (15, 'q', 'quadrillion'),
    (18, 'Q', 'quintillion'),
    (21, 's', 'sextillion'),
    (24, 'S', 'septillion'),
    (27, 'o', 'octillion'),
    (30, 'N', 'nonillion'),
    (33, 'd', 'decillion')
]


def draw_rect(upper_left: Tuple[int, int], lower_right: Tuple[int, int], text: str, horz='-', vert='|', corner='+') -> str:
    """
    Draw a rectangle in a block of text. Block is not extended to make rect fit; the rect coords must lie entirely
    within the given block.
    """
    lines = text.split('\n')
    x1, y1 = upper_left
    x2, y2 = lower_right
    
    if y1 >= len(lines) or y1 < 0:
        raise ValueError("Upper left Y-coord out of bounds: {!r}".format(y1))
    if y2 >= len(lines) or y2 < 0:
        raise ValueError("Lower right Y-coord out of bounds: {!r}".format(y2))
    
    if x1 >= len(lines[y1]) or x1 < 0:
        raise ValueError("Upper left X-coord out of bounds: {!r}".format(x1))
    if x2 >= len(lines[y2]) or x1 < 0:
        raise ValueError("Lower right X-coord out of bounds: {!r}".format(x2))
        
    # correct user error/confusion
    upper_left = (min(x1, x2), min(y1, y2))
    lower_right = (max(x1, x2), max(y1, y2))
    x1, y1 = upper_left
    x2, y2 = lower_right
        
    if y1 == y2:
        if x1 == x2:
            lines[y1] = lines[y1][:x1] + corner + lines[y1][x1 + 1:]
        else:
            # no corners or horz, only vert
            lines[y1] = lines[y1][:x1] + vert + lines[y1][x1 + 1:]
            lines[y1] = lines[y1][:x2] + vert + lines[y1][x2 + 1:]
    else:
        if x1 == x2:
            lines[y1] = lines[y1][:x1] + horz + lines[y1][x1 + 1:]
            lines[y2] = lines[y2][:x1] + horz + lines[y2][x1 + 1:]
        else:
            horz_len = x2 - x1 + 1
            horz_line = corner + (horz * (horz_len - 2)) + corner
            
            # top and bottom:
            lines[y1] = lines[y1][:x1] + horz_line + lines[y1][x2 + 1:]
            lines[y2] = lines[y2][:x1] + horz_line + lines[y2][x2 + 1:]
            
            # verts in between:
            for i in range(1, y2 - y1):
                lines[y1+i] = lines[y1+i][:x1] + vert + lines[y1+i][x1 + 1:]
                lines[y1+i] = lines[y1+i][:x2] + vert + lines[y1+i][x2 + 1:]
                
    return '\n'.join(lines)
    

def money(amt: int, full=False) -> str:
    # TODO: O(1) time func, O(n) is fine for this small number of n but
    # this is DEFINITELY doable in O(1).
    
    
    if amt < (10**NumberNames[0][0]):
        return "${:d}".format(amt)
        
    for n in NumberNames:
        power, suffix, full_name = n
        after = suffix if not full else ' ' + full_name
        
        # if its the last one then can only do that
        if power == NumberNames[-1][0] or amt < (10**(power + 3)):
            return '${:.3f}{:s}'.format(amt/(10**power), after)


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
