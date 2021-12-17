import math
from typing import Optional
from datetime import timedelta
from .format import format_timer, pad_middle, pad_right, pad_left
from .activities import Activity, OwnedActivities

DefaultTextCardWidth = 65
_RightColumnWidth = 14


def progress_bar(
        width: int,
        progress: float,
        end_char: str = '|',
        fill_char: str = '-',
        empty_char: str = ' '
    ) -> str:
    """
    Draw a progress bar that shows the given progress. Will only be full at exactly 100% progress.
    
    :param width: The width of the progress bar, including the ends. The actual progress notches
    will have this width - 2 to fill. If width is less than 3, no progress notches will be in the
    returned string.
    :param progress: The current progress to show. This is a float between 0.0 and 1.0.
    :param end_char: Character to use for the end caps.
    :param fill_char: Character to use for filled progress notches.
    :param empty_char: Character to use for unfilled progress notches.
    """
    notches = width - (len(end_char) * 2) # account for the 'ends' of the prog bar.
    filled = math.floor(notches * progress)
    empty = notches - filled
    text = end_char + (fill_char * filled_notches) + (empty_char * empty_notches) + end_char
    return text


def bar(width=DefaultTextCardWidth) -> str:
    return '+' + ('-' * (width - 2)) + '+'


def make_act_store_listing(act: Activity, count: int, auto_count: int, width=DefaultTextCardWidth) -> str:
    """
    Create a card for the store that shows the price, consumtion, and production
    of the next purchased instance of the Activity.
    
    :param act: The Activity to make the store card for.
    :param count: The current number of owned instances of that activity.
    :param width: The width of the card to produce.
    """
    # +--------------------------------------------------------------+
    # | $20 Eat Bagels               - $100/C (0.00J)  | AUTO x16192 |
    # | 999h60m55s                   + $100/C (0.003J) | x4          |
    # +--------------------------------------------------------------+
    global _RightColumnWidth
    
    # actual avail is width minus 2 for the borders and minus 2 for padding
    lc_text_space = width - _RightColumnWidth - 2 - 2
    
    # left column first (lc)
    # need to do calculation out of order bc + and - should left-align, so
    # calculate the size of both and add right padding to the shorter
    lc_top_right = "- ${:d}/C ({:.2f}J)".format(act.money_cost(count), act.juice_cost(count))
    lc_bot_right = "+ ${:d}/C ({:.4f}J)".format(act.money_rate(count), act.juice_rate(count))
    if len(lc_top_right) > len(lc_bot_right):
        lc_bot_right += (' ' * (len(lc_top_right) - len(lc_bot_right)))
    else:
        lc_top_right += (' ' * (len(lc_bot_right) - len(lc_top_right)))
    
    lc_top_left = "${:d} {:s}".format(act.price(count), act.name)
    lc_top_text = pad_middle(lc_text_space, lc_top_left, lc_top_right)
    
    lc_bot_left = format_timer(act.duration)
    lc_bot_text = pad_middle(lc_text_space, lc_bot_left, lc_bot_right)
    
    
    # on to the right column
    
    # right col will only subtract 1 for border bc one border is shared w left col glub
    # still need to subtract 2 for the padding tho
    rc_text_space = _RightColumnWidth - 1 - 2
    rc_top_text = pad_right(rc_text_space, "AUTO x{:d}".format(2 ** auto_count))
    rc_bot_text = pad_right(rc_text_space, "{:d}i".format(act.auto_price(auto_count)))
    
    
    # now put 'em all together!!!!!!!!
    full_text = ''
    full_text += '| ' + lc_top_text + ' | ' + rc_top_text + ' |\n'
    full_text += '| ' + lc_bot_text + ' | ' + rc_bot_text + ' |'    
    
    return full_text


def make_act_card(oa: OwnedActivities, t: float, width=DefaultTextCardWidth) -> str:
    """
    Create a card that shows the status of an OwnedActivities.
    
    :param oa: The OwnedActivities to make the card for.
    :param t: The current game time represented in seconds since start.
    :param width: The width of the card to produce.
    """
    # +------------------------------------------------+--------------+
    # | Eat Bagels                    ($20) x242193:IN |    (No auto) |
    # | $100 (0J)                     $100/C, 0.03CJ/C |        x{:d} |
    # | |                                 | 999h60m55s |      RUNNING |
    # +------------------------------------------------+--------------+
    global _RightColumnWidth
    
    # LEFT COLUMN
    
    # actual avail is width minus 2 for the borders and minus 2 for padding
    lc_text_space = width - _RightColumnWidth - 2 - 2

    inactive = oa.count - oa.active
    # top line
    lc_top_left = oa.name
    lc_top_right = "(${:d}) x{:d}:{:d}".format(oa.price, oa.active, inactive)
    lc_top_text = pad_middle(lc_text_space, lc_top_left, lc_top_right)
    
    # mid line
    lc_mid_left = "${:d} ({:.2f}J)".format(oa.money_cost, oa.juice_cost)
    lc_mid_right = "${:d}/C {:.4f}J/C".format(oa.money_production, oa.juice_production)
    lc_mid_text = pad_middle(lc_text_space, lc_mid_left, lc_mid_right)
    
    # bot line
    remaining_duration = oa.activity.duration
    if oa.execution is not None:
        remaining_duration = oa.execution.remaining(t)
        prog = oa.execution.progress(t)
        
        max_time_len = 10  # assuming three digits for hour
        prog_bar_len = lc_text_space - max_time_len - 1  # extra 1 for padding between
        lc_bot_left = progress_bar(prog_bar_len, prog)
    else:
        lc_bot_left = 'X'
    lc_bot_right = format_timer(remaining_duration)
    lc_bot_text = pad_middle(lc_text_space, lc_bot_left, lc_bot_right)
    
    
    # RIGHT COLUMN
    
    # right col will only subtract 1 for border bc one border is shared w left col glub
    # still need to subtract 2 for the padding tho
    rc_text_space = _RightColumnWidth - 1 - 2
    
    if oa.automations < 1:
        rc_top_text = pad_left(rc_text_space, "(No auto)")
        rc_mid_text = ' ' * rc_text_space
        rc_bot_text = ' ' * rc_text_space
    else:
        rc_top_text = pad_left(rc_text_space, "AUTO")
        rc_mid_text = pad_left(rc_text_space, "x{:d}".format(oa.automation_bonus))
        if oa.automated:
            rc_bot_text = pad_left(rc_text_space, "RUNNING")
        else:
            rc_bot_text = pad_left(rc_text_space, "(off)")
    
    
    # now put 'em all together!!!!!!!!
    full_text = ''
    full_text += '| ' + lc_top_text + ' | ' + rc_top_text + ' |\n'
    full_text += '| ' + lc_mid_text + ' | ' + rc_mid_text + ' |\n'
    full_text += '| ' + lc_bot_text + ' | ' + rc_bot_text + ' |'
    return full_text
        
    