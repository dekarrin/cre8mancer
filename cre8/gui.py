from .activities import Jobs, Outlets
from .engine import Engine, RulesViolationError
import tkinter as tk

from typing import Tuple

ActionOptionsList = list()
ActionOptionsList += ['-- Select Activity --', '', '-- Jobs --']
ActionOptionsList += [j.name for j in Jobs] + ['-- Outlets --'] + [o.name for o in Outlets]


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
    frm_component = tk.Frame(master=master)
    frm_component.pack(padx=2, pady=2)
    
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
            
        output_func(msg)
        #status_func(msg)

    entry_click_lbl = tk.Button(frm_component, text="Click!", command=do_click)
    entry_click_lbl.pack(side=tk.LEFT)
    

def run_gui(g: Engine):
    root = tk.Tk()
    root.title("Cre8or Forge v0.0a")

    root.rowconfigure(0, minsize=300, weight=1)
    root.columnconfigure(0, minsize=400, weight=1)
    root.rowconfigure(1, minsize=100, weight=0)
    
    frm_output = tk.Frame(master=root)
    output_height = 6
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
    
    def write_status(text: str):
        status.config(state=tk.NORMAL)
        status.delete("0.0", tk.END)
        status.insert("0.0", text)
        status.config(state=tk.DISABLED)
    
    status.pack()

    frm_entry = tk.Frame(master=root)
    frm_entry.grid(row=0, column=1, sticky="nsew")

    build_click_component(g, write_output, write_status, frm_entry)
    
    frm_output.grid(row=1, column=0, columnspan=2, sticky="nsew")

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

#    root.after(0, 
    root.mainloop()