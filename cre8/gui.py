from .activities import Jobs, Outlets
from .engine import Engine, RulesViolationError
import tkinter as tk
from tkinter import ttk
import math

from typing import Tuple, Optional, Union


class Counter(tk.Frame):
    """
    Counter component that can track its own value. Has increment and decrement buttons, or user can directly
    edit the value. Arranged in a horizontal structure such as "[-] [FIELD] [+]".
    
    This component is for int values. For float values, use DoubleCounter.

    To get the field that accepts input, use the 'field' attribute. In general it is better to use the
    get() and set() methods on this component though.
    """
    def __init__(self, master, value=0, inc_amount=1):
        super().__init__(master=master)
        
        self.increment_amount = inc_amount

        self._var = tk.StringVar()
        self._last_valid = value

        dec_button = tk.Button(self, text="-", command=self.decrement)
        dec_button.pack(fill=tk.NONE, side=tk.LEFT)

        self.field = tk.Entry(self, textvariable=self._var)
        self.field.pack(fill=tk.X, side=tk.LEFT)

        inc_button = tk.Button(self, text="+", command=self.increment)
        inc_button.pack(fill=tk.NONE, side=tk.LEFT)
        
        if value is not None:
            self.set(value)
            
    def reset(self):
        """
        Reset the counter to the last valid value it contained, discarding the current
        contents.
        """
        self._var.set(self._last_valid)

    def set(self, value: int):
        """
        Set a new value for the counter.

        :param value: The new value.
        """
        str_val = str(value)
        
        try:
            int(str_val)
            self._last_valid = value
        except ValueError:
            # just dont store it as the last valid value
            pass
        
        self._var.set(str_val)

    def get(self) -> Optional[int]:
        """
        Get the current value of the counter. This will be an int
        if it currently contains a valid numerical value, or None
        if there is not a valid numerical value.
        """
        str_val = self._var.get()
        try:
            val = int(str_val)
            return val
        except ValueError:
            return None

    def decrement(self):
        """
        Decrease the current value by 1. If it is not currently a
        valid value, it is set to the last valid value it was first.
        """
        if self.get() is None:
            self.reset()
        
        self.set(self.get() - self.increment_amount)

    def increment(self):
        """
        Increase the current value by 1.
        """
        old_val = self.get()
        
        if old_val is None:
            self.reset()
            old_val = self.get()
        
        new_val = old_val + self.increment_amount
        self.set(new_val)
        
        
class DoubleCounter(Counter):
    def __init__(self, master, value: float = 0.0, inc_amount: float = 1.0, precision=0.1):
        precision_power = math.log10(precision)
        if not precision_power.is_integer() or precision_power > 0:
            raise ValueError("precision must be given in negative powers of 10, such as 0.1, 0.001, or 0.00001")
        if precision_power == 0:
            raise ValueError("precision of 1 is equivalent to Counter; use that instead")
        self.precision = precision
        
        # precision will get used in set() which is called by super.ctor
        # so make sure to call ctor after precision is setup
        super().__init__(master, value, inc_amount)
        
    def set(self, value: float):
        """
        Set a new value for the counter.

        :param value: The new value.
        """
        # first, if it is zero, we'll get domain errors. we can treat it as a special case.
        if value == 0.0:
            str_val = '.0'
        else:
            # first find number of zeroes between decimal and num, we need to preserve it
            # in formatting
            value_scale = int(math.floor(math.log10(value))) + 1
            if value_scale < 0:
                placeholder_count = (value_scale * -1)
            else:
                placeholder_count = 0
            
            # quantize to precision
            scaled = int(value * (1/self.precision))
            # put placeholders in front
            str_val = ('0' * placeholder_count) + str(scaled)
            
            # now display it with decimal in correct position
            precision_power = int(math.log10(self.precision))
            str_val = str_val[:precision_power] + '.' + str_val[precision_power:]
            
        # check if a zero needs to be added to the left
        if str_val[0] == '.':
            str_val = '0' + str_val
        
        try:
            float(str_val)
            self._last_valid = value
        except ValueError:
            # just dont store it as the last valid value
            pass
        
        self._var.set(str_val)

    def get(self) -> Optional[float]:
        """
        Get the current value of the counter. This will be a float
        if it currently contains a valid numerical value, or None
        if there is not a valid numerical value in it.
        """
        str_val = self._var.get()
        try:
            val = float(str_val)
            return val
        except ValueError:
            return None


class ActivitiesOptionsMenu(tk.OptionMenu):
    def __init__(self, master):
        self._options_list = list()
        self._init_options()
        
        self._var = tk.StringVar()
        self._var.set(self._options_list[0])
        
        super().__init__(master, self._var, *self._options_list)
        self.config(width=20)
        
    def value_as_target(self) -> Tuple[Optional[str], int]:
        """
        Read action options that supplies answer to variable and return
        type and index
        """
        val = self._var.get()
        
        idx = -1
        for j in Jobs:
            idx += 1
            if j.name.lower() == val.lower():
                return 'job', idx
        idx = -1
        for o in Outlets:
            idx += 1
            if o.name.lower() == val.lower():
                return 'outlet', idx
        
        return None, 0        
        
    def _init_options(self):
        self._options_list = list()
        self._options_list.append('-- Select Activity --')
        self._options_list.append('')
        self._options_list.append('-- Jobs --')
        self._options_list += [j.name for j in Jobs]
        self._options_list.append('-- Outlets --')
        self._options_list += [o.name for o in Outlets]

    
class Gui:
    def __init__(self, g: Engine, output_lines: int = 7):
        self.debug_money: Counter
        self.debug_juice: DoubleCounter
        self.debug_seeds: DoubleCounter
        self.debug_ideas: Counter
        
        self.debug_entry_notebook_index: int
        
        self.update_main_content = True
        self.g = g
        self.root = tk.Tk()
        self.root.title("Cre8or Forge v0.0a")
        
        self.mode_button_var = tk.StringVar()
        self.mode_button_var.set("Store")
        self.mode = 'status'
        
        # setup root window config
        self.root.rowconfigure(0, minsize=300, weight=1)
        self.root.columnconfigure(0, minsize=400, weight=1)
        self.root.columnconfigure(1, minsize=200, weight=0)
        self.root.rowconfigure(1, minsize=100, weight=0)
        
        _, self.main_content = self._build_main_content_frame(self.root)
        
        self.entry_frames_notebook = self._build_entry_frames(self.root)
        # Assumes 'Debug' is the last tab added:
        self.debug_entry_notebook_index = self.entry_frames_notebook.index(tk.END) - 1
        
        # setup up output frame and store it for later outputting
        _, self.output = self._build_output_frame(self.root, output_lines)

        # do a single update to get window size then set it as the minimum
        # so user cant resize smaller than the elements
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        
    def run(self):
        self.root.after(0, self._update)
        self.root.mainloop()
    
    def swap_mode(self):
        if self.mode == 'status':
            self.mode = "store"
            self.mode_button_var.set("Status")
        elif self.mode == 'store':
            self.mode = "status"
            self.mode_button_var.set("Store")
        else:
            raise ValueError("Should never happen")
        
    def write_output(self, text: str):
        self.output.config(state=tk.NORMAL)
        self.output.delete("0.0", tk.END)
        self.output.insert("0.0", text)
        self.output.config(state=tk.DISABLED)
        
    def write_main_content(self, text: str):
        self.main_content.config(state=tk.NORMAL)
        self.main_content.delete("0.0", tk.END)
        self.main_content.insert("0.0", text)
        self.main_content.config(state=tk.DISABLED)
        
    def apply_debug(self):
        money = self.debug_money.get()
        juice = self.debug_juice.get()
        seeds = self.debug_seeds.get()
        ideas = self.debug_ideas.get()
        self.g.set_state(money=money, juice=juice, seeds=seeds, ideas=ideas)
        self.entry_frames_notebook.select(0)

    @property
    def in_debug_mode(self) -> bool:
        idx = self.entry_frames_notebook.index(tk.CURRENT)
        return idx == self.debug_entry_notebook_index
        
    def _update(self):
        self.g.update()
        if self.in_debug_mode:
            self.write_main_content("In debug mode. Switch back to the game to resume display")
            self.update_main_content = True
        else:
            # set debug mode stats so it is correct when user swaps to it
            self.debug_money.set(self.g.get_state('money'))
            self.debug_juice.set(self.g.get_state('juice'))
            self.debug_seeds.set(self.g.get_state('seeds'))
            self.debug_ideas.set(self.g.get_state('ideas'))
        
            if self.mode == 'status':
                self.write_main_content(self.g.status())
                self.update_main_content = True  # this must be here in case a swap to store mode occurs
            elif self.mode == 'store':
                if self.update_main_content:
                    self.write_main_content(self.g.show_store())
                    self.update_main_content = False
            else:
                raise ValueError("Should never happen")
        
        self.root.after(500, self._update)
        
    def _build_main_content_frame(self, master) -> Tuple[tk.Widget, tk.Text]:
        """
        Return the fully-configured main content frame with geometry manager
        already set. Additionally, return the Text field that holds the contents
        of text within the main content frame.
        """
        frm_main = tk.Frame(master=master, relief=tk.SUNKEN, borderwidth=3)
        frm_main.grid(row=0, column=0, sticky="nsew")
        mc_field = tk.Text(master=frm_main)
        mc_scrollbar = ttk.Scrollbar(master=frm_main, command=mc_field.yview)
        mc_scrollbar.pack(side=tk.RIGHT, fill="y")
        mc_field['yscrollcommand'] = mc_scrollbar.set
        mc_field.pack(side=tk.RIGHT, fill="x")
        
        return frm_main, mc_field
        
    def _build_entry_frames(self, master) -> tk.Widget:
        entry_frames = ttk.Notebook(master)
        entry_frames.grid(row=0, column=1, sticky="nsew")
        main_entry_frame = self._build_main_entry_frame(entry_frames)
        debug_entry_frame = self._build_debug_entry_frame(entry_frames)

        entry_frames.add(main_entry_frame, text="Game")
        # ensure debug is always the last entry added
        entry_frames.add(debug_entry_frame, text="Debug")
        return entry_frames
        
    def _build_main_entry_frame(self, master) -> tk.Frame:
        """
        Return the fully-configured and packed main entry frame.
        """
        main_entry_frame = tk.Frame(master=master)
        main_entry_frame.pack(fill=tk.BOTH, expand=True)
        self._build_click_component(main_entry_frame)
        self._build_buy_component(main_entry_frame)
        frm_mode_buttons = tk.Frame(master=main_entry_frame)
        frm_mode_buttons.pack(side=tk.TOP)
        mode_btn = tk.Button(frm_mode_buttons, textvariable=self.mode_button_var, command=self.swap_mode)
        mode_btn.pack(side=tk.LEFT)
        return main_entry_frame
        
    def _build_click_component(self, master) -> tk.Frame:
        """
        Return the fully-configured and packed click component frame.
        """
        frm_component = tk.Frame(master=master)
        frm_component.pack(side=tk.TOP)
        
        opts_menu = ActivitiesOptionsMenu(frm_component)
        opts_menu.pack(side=tk.LEFT)
        
        def do_click():
            target_type, target_idx = opts_menu.value_as_target()
            if target_type is None:
                self.write_output("Select a valid option first")
                return
            
            try:
                msg = self.g.click(target_type, target_idx)
            except RulesViolationError as ex:
                self.write_output(str(ex))
                return
            
            self.write_output(msg)
            self.g.update()
            self.write_main_content(self.g.status())

        entry_click_lbl = tk.Button(frm_component, text="Click!", command=do_click)
        entry_click_lbl.pack(side=tk.LEFT)
        return frm_component

    def _build_buy_component(self, master) -> tk.Frame:
        """
        Return the fully-configured and packed buy component frame.
        """
        frm_component = tk.Frame(master=master)
        frm_component.pack(side=tk.TOP)
        
        opts_menu = ActivitiesOptionsMenu(frm_component)
        opts_menu.pack(side=tk.LEFT)
        
        def do_buy():
            target_type, target_idx = opts_menu.value_as_target()
            if target_type is None:
                self.write_output("Select a valid option first")
                return
            
            try:
                msg = self.g.buy('instance', target_type, target_idx)
            except RulesViolationError as ex:
                self.write_output(str(ex))
                return
            
            self.write_output(msg)
            self.g.update()
            self.write_main_content(self.g.status())

        entry_click_lbl = tk.Button(frm_component, text="Buy", command=do_buy)
        entry_click_lbl.pack(side=tk.LEFT)
        return frm_component
        
    def _build_debug_entry_frame(self, master) -> tk.Frame:
        """
        Return the fully-configured and packed debug entry frame.
        """
        debug_entry_frame = tk.Frame(master=master)
        debug_entry_frame.pack(fill=tk.BOTH, expand=True)
        debug_entry_frame.columnconfigure(0, minsize=50, weight=0)
        debug_entry_frame.columnconfigure(1, weight=1)
        
        lbl_debug_money = tk.Label(debug_entry_frame, text="Money:")
        lbl_debug_money.grid(row=0, column=0)
        self.debug_money = Counter(master=debug_entry_frame)
        self.debug_money.grid(row=0, column=1)
        
        lbl_debug_juice = tk.Label(debug_entry_frame, text="Juice:")
        lbl_debug_juice.grid(row=1, column=0)
        self.debug_juice = DoubleCounter(debug_entry_frame, inc_amount=0.01, precision=0.0001)
        self.debug_juice.grid(row=1, column=1)
        
        lbl_debug_seeds = tk.Label(debug_entry_frame, text="Seeds:")
        lbl_debug_seeds.grid(row=2, column=0)
        self.debug_seeds = DoubleCounter(debug_entry_frame, inc_amount=0.01, precision=0.000001)
        self.debug_seeds.grid(row=2, column=1)
        
        lbl_debug_ideas = tk.Label(debug_entry_frame, text="(i)deas:")
        lbl_debug_ideas.grid(row=3, column=0)
        self.debug_ideas = Counter(debug_entry_frame)
        self.debug_ideas.grid(row=3, column=1)
        
        btn_apply = tk.Button(debug_entry_frame, text="Apply", command=self.apply_debug)
        btn_apply.grid(row=5, column=0)
        return debug_entry_frame
        
    def _build_output_frame(self, master, output_lines) -> Tuple[tk.Widget, tk.Text]:
        """
        Return the fully-configured output frame with geometry manager
        already set. Additionally, return the Text field that holds the contents
        of text within the output frame.
        """
        frm = tk.Frame(master=self.root)
        frm.grid(row=1, column=0, columnspan=2, sticky="nsew")
        output = tk.Text(master=frm, height=output_lines, width=103)
        output.config(state=tk.DISABLED)
        output.pack()
        return frm, output
