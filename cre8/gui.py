from .activities import Jobs, Outlets
import tkinter as tk

ActionOptionsList = ['-- Select Activity --', '', '-- Jobs --'] + [j.name for j in Jobs] + [o.name for o in Outlets]


def make_act_options_menu(master): tk.StringVar:
    global ActionOptionsList
        
    variable = tk.StringVar()
    variable.set(opts[0])
    
    opts_menu = tk.OptionMenu(master, variable, *ActionOptionsList)
    opts_menu.pack(side=tk.LEFT)
    return variable

def read_act_options(variable: tk.StringVar) -> Tuple[str, str]:
    """
    Read action options that supplies answer to variable and return
    type and index
    """
    val = variable.get()
    
    idx = 0
    for j in Jobs:
        idx += 1
        if j.name.lower() = val.lower():
            return 'job', idx
    idx = 0
    for o in Outlets:
        idx += 1
        if o.name.lower() == val.lower():
            return 'outlet', idx


def exec_click(    

def build_click_component(master):
    frm_component = tk.Frame(master=master)
    frm_component.pack(padx=2, pady=2)
    
    click_opt_var = make_act_options_menu(frm_component)

    entry_click_lbl = tk.Label(frm_component, text="Click!")
    entry_click_lbl.pack(side=tk.LEFT)
    

def run_gui():
    root = tk.Tk()
    root.title("Cre8or Forge v0.0a")

    root.rowconfigure(0, minsize=300, weight=1)
    root.columnconfigure(0, minsize=400, weight=1)
    root.rowconfigure(1, minsize=100, weight=1)

    frm_status = tk.Frame(master=root, relief=tk.SUNKEN, borderwidth=3)
    frm_status.grid(row=0, column=0, sticky="nsew")

    frm_entry = tk.Frame(master=root)
    frm_entry.grid(row=0, column=1, sticky="nsew")

    build_click_component(frm_entry)

    frm_output = tk.Frame(master=root, bg="blue")
    frm_output.grid(row=1, column=0, columnspan=2, sticky="nsew")

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

    root.mainloop()