import math
from typing import Optional
from datetime import timedelta
from .format import format_timer

DefaultTextCardWidth = 50

def bar(width=DefaultTextCardWidth):
    return '+' + ('-' * (width - 2)) + '+'

# TODO: refactor this and make_act_card to take arguments in same order as
# Activity
def make_act_store_listing(
    name: str,
    price_for_next: float,
    cost_per_run: int,
    juice_required: float,
    money_produced: int,
    juice_produced: float,
    duration: timedelta,
    card_width=DefaultTextCardWidth
):
    # +------------------------------------------------+
    # | $20 Eat Bagels               - $100/C (0.00J)  |
    # | 999h60m55s                   + $100/C (0.003J) |
    # +------------------------------------------------+
    
    card_text_space = card_width - 2 - 2
    
    # need to do calculation out of order bc + and - should left-align, so
    # calculate the size of both and add right padding to the shorter
    top_right = "- ${:d}/C ({:.2f}J)".format(cost_per_run, juice_required)
    bot_right = "+ ${:d}/C ({:.4f}J)".format(money_produced, juice_produced)
    if len(top_right) > len(bot_right):
        bot_right += (' ' * (len(top_right) - len(bot_right)))
    else:
        top_right += (' ' * (len(bot_right) - len(top_right)))
    
    top_left = "${:d} {:s}".format(price_for_next, name)
    top_text_len = len(top_left) + len(top_right)
    top_space_needed = card_text_space - top_text_len
    top_text = top_left + (' ' * top_space_needed) + top_right
    
    bot_left = format_timer(duration)
    bot_text_len = len(bot_left) + len(bot_right)
    bot_space_needed = card_text_space - bot_text_len
    bot_text = bot_left + (' ' * bot_space_needed) + bot_right
    
    # now put 'em all together!!!!!!!!
    full_text = ''
    full_text += '| ' + top_text + ' |\n'
    full_text += '| ' + bot_text + ' |'
    return full_text

def make_act_card(
    name: str,
    price_for_next: float,
    count: int,
    active: int,
    cost_per_run: int,
    juice_required: float,
    money_produced: int,
    juice_produced: float,
    execution_prog: Optional[float],
    remaining_duration: timedelta,
    card_width=DefaultTextCardWidth
):
    # +------------------------------------------------+
    # | Eat Bagels                    ($20) x242193:IN |
    # | $100 (0J)                     $100/C, 0.03CJ/C |
    # | |                                 | 999h60m55s |
    # +------------------------------------------------+
    
    # -2 for padding, -2 for borders
    card_text_space = card_width - 2 - 2

    inactive = count - active
    # top line
    top_left = name
    top_right = "(${:d}) x{:d}:{:d}".format(price_for_next, active, inactive)
    top_text_len = len(top_left) + len(top_right)
    top_space_needed = card_text_space - top_text_len
    top_text = top_left + (' ' * top_space_needed) + top_right
    
    # mid line
    mid_left = "${:d} ({:.2f}J)".format(cost_per_run, juice_required)
    mid_right = "${:d}/C {:.4f}J/C".format(money_produced, juice_produced)
    mid_text_len = len(mid_left) + len(mid_right)
    mid_space_needed = card_text_space - mid_text_len
    mid_text = mid_left + (' ' * mid_space_needed) + mid_right
    
    # bot line
    if execution_prog is not None:
        max_time_len = 10  # assuming three digits for hour
        prog_bar_len = card_text_space - max_time_len - 1  # extra 1 for padding between
        prog_notches = prog_bar_len - 2  # account for the 'ends' of the prog bar.
        filled_notches = math.floor(prog_notches * execution_prog)
        empty_notches = prog_notches - filled_notches
        bot_left = '|' + ('-' * filled_notches) + (' ' * empty_notches) + '|'
    else:
        bot_left = 'X'
    bot_right = format_timer(remaining_duration)
    bot_text_len = len(bot_left) + len(bot_right)
    bot_space_needed = card_text_space - bot_text_len
    bot_text = bot_left + (' ' * bot_space_needed) + bot_right
    
    # now put 'em all together!!!!!!!!
    full_text = ''
    full_text += '| ' + top_text + ' |\n'
    full_text += '| ' + mid_text + ' |\n'
    full_text += '| ' + bot_text + ' |'
    return full_text
        
    