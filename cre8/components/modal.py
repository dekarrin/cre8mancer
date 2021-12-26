import tkinter as tk
from tkinter import ttk
from typing import Callable, Any, Optional
import os.path

_warn_path = os.path.join(os.path.dirname(__file__), 'warning.png')
_warn_pi: tk.PhotoImage = None


def _get_warn_image() -> tk.PhotoImage:
    global _warn_pi
    if _warn_pi is None:
        _warn_pi = tk.PhotoImage(file=_warn_path)
    return _warn_pi


class ModalBox(tk.Toplevel):
    def __init__(self, master):
        self._master_widget = master
        super().__init__(master)
        
    def make_modal(self):
        self.focus_set()
        self.grab_set()
        self.transient(self._master_widget)
        self.wait_window(self)
        
    
class ConfirmBox(ModalBox):
    def __init__(
        self,
        master,
        text: str,
        bind: Optional[Callable[[bool], Any]] = None,
        title: Optional[str] = None,
        yes: str = 'Yes',
        no: str = 'No',
        default_no: bool = False
    ):
        super().__init__(master)
        
        if title:
            self.title(title)
        
        self._select_func = bind
        
        message_frame = tk.Frame(master=self)
        message_frame.pack(side=tk.TOP)
        
        
        image_label = tk.Label(message_frame, image=_get_warn_image())
        image_label.pack(side=tk.LEFT)
        
        text_label = tk.Label(message_frame, text=text)
        text_label.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(master=self)
        button_frame.pack(side=tk.TOP)
        
        no_button = tk.Button(master=button_frame, text=no, command=self._no)
        no_button.pack(side=tk.RIGHT)
        yes_button = tk.Button(master=button_frame, text=yes, command=self._yes)
        yes_button.pack(side=tk.RIGHT)
        
        if default_no:
            no_button.focus_set()
        else:
            yes_button.focus_set()

        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        self.maxsize(self.winfo_width(), self.winfo_height())
        
    def _no(self):
        select_func = self._select_func
        self.destroy()
        select_func(False)
        
    def _yes(self):
        select_func = self._select_func
        self.destroy()
        select_func(True)
    

        
def confirm(
    text: str,
    title: Optional[str] = None,
    yes: str = 'Yes',
    no: str = 'No',
    default_no: bool = False
) -> bool:
    result = False
    
    def on_select(value):
        nonlocal result
        result = value
        
    conf_box = ConfirmBox(
        master=None, text=text, title=title, yes=yes, no=no, default_no=default_no, bind=on_select
    )
    
    conf_box.make_modal()
    return result