from .activities import Jobs, Outlets
from .engine import Engine, RulesViolationError
import tkinter as tk
from tkinter import ttk

from typing import Tuple


class ActivitiesOptionsMenu(tk.OptionMenu):
    def __init__(self, master):
        self._options_list = list()
        self._init_options()
        
        self._var = tk.StringVar()
        self._var.set(self._options_list[0])
        
        super().__init__(master, self._var, *self._options_list)
        self.config(width=20)
        
    def value_as_target(self) -> Tuple[str, int]:
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
        self.root.rowconfigure(1, minsize=100, weight=0)
        
        # setup main content frame and store it for later outputting
        frm_main = tk.Frame(master=self.root, relief=tk.SUNKEN, borderwidth=3)
        frm_main.grid(row=0, column=0, sticky="nsew")
        self.main_content = tk.Text(master=frm_main)
        mc_scrollbar = ttk.Scrollbar(master=frm_main, command=self.main_content.yview)
        mc_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.main_content['yscrollcommand'] = mc_scrollbar.set
        self.main_content.pack(side=tk.RIGHT, fill="x")
        
        # setup entry frame
        frm_entry = tk.Frame(master=self.root)
        frm_entry.grid(row=0, column=1, sticky="nsew")
        self._build_click_component(frm_entry)
        self._build_buy_component(frm_entry)
        mode_btn = tk.Button(frm_entry, textvariable=self.mode_button_var, command=self.swap_mode)
        mode_btn.pack(side=tk.TOP)
        
        # setup up output frame and store it for later outputing
        frm_output = tk.Frame(master=self.root)
        frm_output.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.output = tk.Text(master=frm_output, height=output_lines, width=103)
        self.output.config(state=tk.DISABLED)
        self.output.pack()

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
        
    def _build_click_component(self, master):
        frm_component = tk.Frame(master=master)
        frm_component.pack(side=tk.TOP, padx=2, pady=2)
        
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

    def _build_buy_component(self, master):
        frm_component = tk.Frame(master=master)
        frm_component.pack(side=tk.TOP, padx=2, pady=2)
        
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
        
    def _update(self):
        self.g.update()
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