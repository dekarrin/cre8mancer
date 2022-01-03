import tkinter as tk
from tkinter import ttk

from typing import Optional, Tuple

from .queryableopts import QueryableOptionMenu


class Window(tk.Toplevel):
    """
    A top-level window with prev and next buttons that shows a flow of information.
    The steps are advanced through when the user clicks the next button, and goes
    back when the user clicks the prev button.
    
    This window looks like the main window of cre8or forge, with a main content
    pane and an output pane. The entry area containsthe next and prev
    buttons as well as a section selector.
    
    Once it is created, add all desired steps, then call start() to begin the flow.
    """
    def __init__(self, master, intro_text="Press 'Next' to get started", intro_section="Start", content_size=(644, 200)):
        super().__init__(master)
        
        self._steps = list()
        self._next_button: tk.Button
        self._prev_button: tk.Button
        
        self._ignore_selector_change = False
        self._section_selector_frame: tk.Frame
        self._section_selector: Optional[QueryableOptionMenu] = None
        self._sections = list()
        
        self._step_index = 0
        self.add_step(output=intro_text, section=intro_section)
        
        self.rowconfigure(0, minsize=50, weight=1)
        self.columnconfigure(0, minsize=50, weight=1)
        self.columnconfigure(1, minsize=200, weight=0)
        self.rowconfigure(1, minsize=100, weight=0)
        
        content_frame, self.main_content, content_sb = self._create_main_content_frame(self)
        entry_frame = self._create_entry_frame(self)
        output_frame, self.output = self._create_output_frame(self, 7)
        
        content_frame.grid(row=0, column=0, sticky="nsew")
        entry_frame.grid(row=0, column=1, sticky="nsew")
        output_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        self.update()
        desired_width = content_size[0] + content_sb.winfo_width() + entry_frame.winfo_width()
        desired_height = content_size[1] + output_frame.winfo_height()
        window_size = str(desired_width) + "x" + str(desired_height)
        self.geometry(window_size)
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        self.maxsize(self.winfo_width(), self.winfo_height())
        
    def add_step(self, output: Optional[str] = None, content: Optional[str] = None, section: Optional[str] = None):
        """
        Add a step to the flow. Steps will be displayed to the user in the
        order that they are added.
        
        :param output: What to show in the output pane. Set to None to leave the
        output pane unmodified from any previous text. Set to an empty string to
        erase the output pane of any previous text.
        :param content: What to show in the main content pane. Set to None to
        leave the main content pane unmodified from any previous text. Set to an
        empty string to erase the content pane of any previous text.
        :param section: If set, the step marks the beginning of a new section
        that is called the value of section. The user can jump to that step by
        selecting that name from the drop-down section selector. Each section
        name must be unique.
        """
        # this assumes that the first call to add_step includes a section.
        # so far this assumption is ensured by the __init__ function.
        if section is None:
            cur_section = self._sections[-1][0]
        else:
            self._sections.append((section, len(self._steps)))
            cur_section = section
            
        step = {
            'output': '',
            'content': '',
            'section': cur_section
        }
        
        # instead of leaving as None when specified, give it same text
        # as prev step. This will make hitting prev way easier since
        # the entire step chain doesnt need to get replayed just to find
        # out what is empty and what isnt on prev step.
        prev_step = None
        if len(self._steps) > 0:
            prev_step = self._steps[-1]
        
        if output is None:
            if prev_step is not None:
                step['output'] = prev_step['output']
        else:
            step['output'] = str(output)
        
        if content is None:
            if prev_step is not None:
                step['content'] = prev_step['content']
        else:
            step['content'] = str(content)
            
        self._steps.append(step)
        
    def start(self):
        """
        Start flow from the beginning. Once called, more sections
        cannot be added.
        """
        if self._section_selector is None:
            sec_names = [x[0] for x in self._sections]
            self._section_selector = QueryableOptionMenu(self._section_selector_frame, *sec_names)
            self._section_selector.pack(side=tk.TOP, fill=tk.X)
            self._section_selector.bind_change(self._section_selected)
        
        self._step_index = -1
        self.next()
        
    def next(self):
        """
        Show the next step.
        """
        self._step_index += 1
        self._run_current_step()
        
    def prev(self):
        """
        Show the previous step.
        """
        self._step_index -= 1
        self._run_current_step()
        
    def write_output(self, text: str):
        self.output.config(state=tk.NORMAL)
        self.output.delete("0.0", tk.END)
        self.output.insert("0.0", text)
        self.output.config(state=tk.DISABLED)
        
    def write_main_content(self, text: str):
        scroll_top, _ = self.main_content.yview()
        self.main_content.config(state=tk.NORMAL)
        self.main_content.delete("0.0", tk.END)
        self.main_content.insert("0.0", text)
        self.main_content.config(state=tk.DISABLED)
        self.main_content.yview_moveto(scroll_top)
        
    def _run_current_step(self):
        """
        Perform the instructions in the current flow step and set the prev and
        next buttons as enabled or disabled based on the current step index.
        """
        if self._step_index >= len(self._steps):
            self._step_index = len(self._steps) - 1
        if self._step_index < 0:
            self._step_index = 0
            
        step = self._steps[self._step_index]
        
        self.write_output(step['output'])
        self.write_main_content(step['content'])
            
        if self._step_index > 0:
            self._prev_button.config(state=tk.NORMAL)
        else:
            self._prev_button.config(state=tk.DISABLED)
            
        if self._step_index + 1 < len(self._steps):
            self._next_button.config(state=tk.NORMAL)
        else:
            self._next_button.config(state=tk.DISABLED)
            
        if step['section'] != self._section_selector.get():
            self._ignore_selector_change = True
            self._section_selector.set(step['section'])
            self._ignore_selector_change = False
            
    def _section_selected(self, *args):
        if self._ignore_selector_change:
            return
        selected_idx = self._section_selector.get_index()
        sec_name, step_idx = self._sections[selected_idx]
        self._step_index = step_idx
        self._run_current_step()
        
    def _create_main_content_frame(self, master) -> Tuple[tk.Widget, tk.Text, tk.Widget]:
        """
        Return the main content frame with all children configured. Additionally,
        return the Text field that holds the contents of text within the main
        content frame.
        
        The returned frame will not have had its geometry manager set.
        """
        frm_main = tk.Frame(master=master, relief=tk.SUNKEN, borderwidth=3)
        mc_field = tk.Text(master=frm_main)
        mc_scrollbar = ttk.Scrollbar(master=frm_main, command=mc_field.yview)
        mc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        mc_field['yscrollcommand'] = mc_scrollbar.set
        mc_field.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        
        return frm_main, mc_field, mc_scrollbar
        
    def _create_entry_frame(self, master) -> Tuple[tk.Frame]:
        """
        Return the entry frame with all children configured. Additionally,
        the previous and next buttons and the section selector frame that
        were created are stored in self so their state can be updated later.
        
        The returned frame will not have had its geometry manager set.
        """
        entry_frame = tk.Frame(master=master)
        
        self._section_selector_frame = tk.Frame(master=entry_frame, borderwidth=3, relief=tk.GROOVE)
        self._section_selector_frame.pack(side=tk.TOP, fill=tk.X, padx=4, pady=4)
        lbl_select = tk.Label(master=self._section_selector_frame, text="Section:")
        lbl_select.pack(side=tk.TOP)
        
        
        frm_bot_buttons = tk.Frame(master=entry_frame)
        frm_bot_buttons.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._next_button = tk.Button(master=frm_bot_buttons, text="Next ->", command=self.next)
        self._next_button.pack(side=tk.RIGHT)
        
        self._prev_button = tk.Button(master=frm_bot_buttons, text="<- Prev", command=self.prev)
        self._prev_button.pack(side=tk.LEFT)
        
        return entry_frame
        
    def _create_output_frame(self, master, output_lines) -> Tuple[tk.Widget, tk.Text]:
        """
        Return the output frame with all children configured. Additionally,
        return the Text field that holds the contents of text within the
        output frame.
        
        The returned frame will not have had its geometry manager set.
        """
        frm = tk.Frame(master=master)
        output = tk.Text(master=frm, height=output_lines, wrap=tk.WORD)
        output.config(state=tk.DISABLED)
        output.pack(fill=tk.X)
        return frm, output