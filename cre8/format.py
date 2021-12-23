import math
from datetime import timedelta

from typing import Tuple, Optional, Sequence

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


class Draw:
    """
    Contains functions for drawing on text. All operations will modify this text unless mutate is set to false.
    """

    def __init__(self, text: str = '', mutate: bool = True):
        """
        Create a new Draw object. If mutate set to true, calls to methods on this Draw will update self.text.

        self.mutate can be changed after construction to alter the Draw's behavior.

        :param text: The initial text. This will be what all operations are applied to.
        :param mutate: Whether operations update self.text. If set to False, calling an operation only returns the
        modified version, it doesn't cause self.text to be updated.
        """
        self.mutate = mutate
        self.text = text

        self.vert_char = '|'
        self.horz_char = '-'
        self.corner_char = '*'

    def copy(self) -> 'Draw':
        new_draw = Draw(self.text, self.mutate)
        new_draw.vert_char = self.vert_char
        new_draw.horz_char = self.horz_char
        new_draw.corner_char = self.corner_char
        return new_draw

    def overtype(self, pos: Tuple[int, int], new_text: str, respect_lines=True) -> str:
        """
        Add new text starting at the given position, replacing any characters that already existed. By default, if this
        ends up adding characters past the previous end of the line, the line is extended to include the new characters.
        This can be altered with the respect_lines parameter.

        If mutate is set to true, calling this function will update self.text to the value it returns; otherwise, this
        function only returns the transformed text and does not save it to self.text

        :param pos: The position in x, y format of the character position within the line and the line to modify.
        :param new_text: The new text to add.
        :param respect_lines: If this is set to False, writing past the end of the line does not extend the line length,
        and instead will overtype the new line character itself. Not a typical use case.
        :return: The transformed text.
        """
        if len(new_text) < 1:
            return self.text

        lines = self.text.split('\n')

        x, y = pos

        if y < 0 or y >= len(lines):
            raise ValueError("Y coordinate out of range: {!r}".format(y))
        if x < 0 or x >= len(lines[y]):
            raise ValueError("X coordinate out of range: {!r}".format(x))

        if not respect_lines:
            start = 0
            # add up length of all lines prior to actual line and add that to x to get total position within string
            for i in range(y):
                start += len(lines[i])
                start += 1  # for the newline char
            start += x
            result = self.text[:start] + new_text + self.text[start + len(new_text):]
        else:
            lines[y] = lines[y][:x] + new_text + lines[y][x + len(new_text):]
            result = '\n'.join(lines)

        if self.mutate:
            self.text = result
        return result

    def overtype_lines(self, starting_pos: Tuple[int, int], new_lines: Sequence[str], respect_lines=True) -> str:
        """
        Overtype several lines at once. This calls overtype with a successively increasing y position for each line
        given, starting at the starting_pos.

        If mutate is set to true, calling this function will update self.text to the value it returns; otherwise, this
        function only returns the transformed text and does not save it to self.text

        :param starting_pos: The position of the first line.
        :param new_lines: The content to overtype each line with.
        :param respect_lines: Set to false to no longer respect line endings for each line. Since this could cause one
        line to overtype into areas that are then overtyped by the next line, this could result in strange behavior.
        """
        x, y = starting_pos

        if y < 0 or y >= self.line_count:
            raise ValueError("Y coordinate out of range: {!r}".format(y))
        if y + len(new_lines) >= self.line_count:
            raise ValueError("Too many lines given; can only have up to {!r} but got {!r}".format(self.line_count - y - 1, len(new_lines)))

        # mutation is required to do every line; ensure it is on without altering this object by creating a secondary
        # draw object.
        # BE CAREFUL NOT TO CAUSE A RECURSIVE CALL
        mutator = self.copy()
        mutator.mutate = True
        for i, line in enumerate(new_lines):
            mutator.overtype((x, y + i), line, respect_lines=respect_lines)

        if self.mutate:
            self.text = mutator.text
        return mutator.text

    def rect(self, upper_left: Tuple[int, int], lower_right: Tuple[int, int]) -> str:
        """
        Draw a rectangle in the text. Block is not extended to make rect fit; the rect coords must lie entirely
        within the given block.

        If mutate is set to true, calling this function will update self.text to the value it returns; otherwise, this
        function only returns the transformed text and does not save it to self.text

        :param upper_left: Coordinates of upper_left corner (inclusive).
        :param lower_right: Coordinates of lower_right corner (inclusive).
        :return: The transformed text.
        """

        lines = self.text.split('\n')
        x1, y1 = upper_left
        x2, y2 = lower_right

        if y1 >= len(lines) or y1 < 0:
            raise ValueError("Upper left Y-coord out of bounds: {!r}".format(y1))
        if y2 >= len(lines) or y2 < 0:
            raise ValueError("Lower right Y-coord out of bounds: {!r}".format(y2))

        # TODO: dont assume a uniform line length.
        # We would actually want to check len of EACH line we intend to
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
                lines[y1] = lines[y1][:x1] + self.corner_char + lines[y1][x1 + 1:]
            else:
                # no corners or horz, only vert
                lines[y1] = lines[y1][:x1] + self.vert_char + lines[y1][x1 + 1:]
                lines[y1] = lines[y1][:x2] + self.vert_char + lines[y1][x2 + 1:]
        else:
            if x1 == x2:
                lines[y1] = lines[y1][:x1] + self.horz_char + lines[y1][x1 + 1:]
                lines[y2] = lines[y2][:x1] + self.horz_char + lines[y2][x1 + 1:]
            else:
                horz_len = x2 - x1 + 1
                horz_line = self.corner_char + (self.horz_char * (horz_len - 2)) + self.corner_char

                # top and bottom:
                lines[y1] = lines[y1][:x1] + horz_line + lines[y1][x2 + 1:]
                lines[y2] = lines[y2][:x1] + horz_line + lines[y2][x2 + 1:]

                # verts in between:
                for i in range(1, y2 - y1):
                    lines[y1+i] = lines[y1+i][:x1] + self.vert_char + lines[y1+i][x1 + 1:]
                    lines[y1+i] = lines[y1+i][:x2] + self.vert_char + lines[y1+i][x2 + 1:]

        result = '\n'.join(lines)
        if self.mutate:
            self.text = result

        return result

    @property
    def line_count(self) -> int:
        """
        Returns the number of lines in the current text.
        """
        return len(self.text.split('\n')) + 1

    

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
