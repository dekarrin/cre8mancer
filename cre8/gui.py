from .activities import Jobs, Outlets
from .engine import Engine, RulesViolationError
import tkinter as tk
from tkinter import ttk

from typing import Tuple

ActionOptionsList = list()
ActionOptionsList += ['-- Select Activity --', '', '-- Jobs --']
ActionOptionsList += [j.name for j in Jobs] + ['-- Outlets --'] + [o.name for o in Outlets]


# TODO: this entire module would be much better as a class

def make_act_options_menu(master) -> tk.StringVar:
    global ActionOptionsList
        
    variable = tk.StringVar()
    variable.set(ActionOptionsList[0])
    
    opts_menu = tk.OptionMenu(master, variable, *ActionOptionsList)
    opts_menu.pack(side=tk.LEFT)
    opts_menu.config(width=20)
    return variable

def read_act_options(variable: tk.StringVar) -> Tuple[str, int]:
    """
    Read action options that supplies answer to variable and return
    type and index
    """
    val = variable.get()
    
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
    

def build_click_component(g: Engine, output_func, status_func, master):
    global mode, modeBtnVar
    frm_component = tk.Frame(master=master)
    frm_component.pack(side=tk.TOP, padx=2, pady=2)
    
    click_opt_var = make_act_options_menu(frm_component)
    def do_click():
        target_type, target_idx = read_act_options(click_opt_var)
        if target_type is None:
            output_func("Select a valid option first")
            return
        
        try:
            msg = g.click(target_type, target_idx)
        except RulesViolationError as ex:
            output_func(str(ex))
            return
        
        mode = "status"
        modeBtnVar.set("Store")
        output_func(msg)
        g.update()
        status_func(g.status())

    entry_click_lbl = tk.Button(frm_component, text="Click!", command=do_click)
    entry_click_lbl.pack(side=tk.LEFT)
    

    
def build_buy_component(g: Engine, output_func, status_func, master):
    global mode, modeBtnVar
    frm_component = tk.Frame(master=master)
    frm_component.pack(side=tk.TOP, padx=2, pady=2)
    
    opt_var = make_act_options_menu(frm_component)
    def do_buy():
        target_type, target_idx = read_act_options(opt_var)
        if target_type is None:
            output_func("Select a valid option first")
            return
        
        try:
            msg = g.buy('instance', target_type, target_idx)
        except RulesViolationError as ex:
            output_func(str(ex))
            return
        
        mode = "status"
        modeBtnVar.set("Store")
        output_func(msg)
        g.update()
        status_func(g.status())

    entry_click_lbl = tk.Button(frm_component, text="Buy", command=do_buy)
    entry_click_lbl.pack(side=tk.LEFT)
    

    
mode = "status"
modeBtnVar: tk.StringVar
updating = True

def set_mode(new_mode: str):
    global mode, modeBtnVar, updating
    
    if new_mode == 'status':
        mode = 'status'
        modeBtnVar.set("Store")
        if not updating:
            updating = True
            

def build_mode_component(g: Engine, output_func, status_func, master):
    global mode, modeBtnVar
    
    def swap_mode():
        global mode, modeBtnVar
        
        if mode == 'status':
            mode = "store"
            modeBtnVar.set("Status")
        elif mode == 'store':
            mode = "status"
            modeBtnVar.set("Store")
        else:
            raise ValueError("Should never happen")
    
    btn = tk.Button(master, textvariable=modeBtnVar, command=swap_mode)
    btn.pack(side=tk.TOP)
    
    

def run_gui(g: Engine):
    global mode, modeBtnVar
    
    root = tk.Tk()
    root.title("Cre8or Forge v0.0a")
    
    modeBtnVar = tk.StringVar()
    modeBtnVar.set("Store")
    mode = "status"

    root.rowconfigure(0, minsize=300, weight=1)
    root.columnconfigure(0, minsize=400, weight=1)
    root.rowconfigure(1, minsize=100, weight=0)
    
    frm_output = tk.Frame(master=root)
    output_height = 7
    output = tk.Text(master=frm_output, height=output_height, width=103)
    output.config(state=tk.DISABLED)
    
    def write_output(text: str):
        output.config(state=tk.NORMAL)
        output.delete("0.0", tk.END)
        output.insert("0.0", text)
        output.config(state=tk.DISABLED)
    
    output.pack()

    frm_status = tk.Frame(master=root, relief=tk.SUNKEN, borderwidth=3)
    frm_status.grid(row=0, column=0, sticky="nsew")
    status = tk.Text(master=frm_status)
    status_sb = ttk.Scrollbar(master=frm_status, command=status.yview)
    status_sb.pack(side=tk.RIGHT, fill="y")
    status['yscrollcommand'] = status_sb.set
    
    def write_status(text: str):
        status.config(state=tk.NORMAL)
        status.delete("0.0", tk.END)
        status.insert("0.0", text)
        status.config(state=tk.DISABLED)
    
    status.pack(side=tk.RIGHT, fill="x")

    frm_entry = tk.Frame(master=root)
    frm_entry.grid(row=0, column=1, sticky="nsew")

    build_click_component(g, write_output, write_status, frm_entry)
    build_buy_component(g, write_output, write_status, frm_entry)
    build_mode_component(g, write_output, write_status, frm_entry)
    
    frm_output.grid(row=1, column=0, columnspan=2, sticky="nsew")

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    def update_status():
        global mode
        
        g.update()
        if mode == 'status':
            write_status(g.status())
            root.after(500, update_status)
        elif mode == 'store':
            write_status(g.show_store())
        else:
            raise ValueError("Should never happen")
        
    root.after(0, update_status)
    root.mainloop()