import tkinter as tk


class QueryableOptionMenu(tk.OptionMenu):
    def __init__(self, master, *options):
        """
        Create new QueryableOptionMenu with the given options. Each option must be unique.
        """
        # Make sure user passed in unique options only
        seen_opts = set()
        for opt in options:
            if opt in seen_opts:
                raise ValueError("Duplicate option {!r}; every option must be unique".format(opt))
            seen_opts.add(opt)
        
        self._options_list = options
        self._var = tk.StringVar()
        self._var.set(self._options_list[0])
        super().__init__(master, self._var, *self._options_list)
        
    def bind_change(self, callback):
        self._var.trace('w', callback)
        
    def get(self) -> str:
        """
        Get the current value of the option menu.
        """
        return self._var.get()
        
    def get_index(self) -> int:
        """
        Get the current index that is selected.
        """
        cur_val = self.get()
        for idx, val in enumerate(self._options_list):
            if val == cur_val:
                return idx
        raise ValueError("currently selected value is not in the initial options")
        
    def set(self, new_value: str) -> str:
        """
        Set the current value of the option menu. It should be one of the options
        originally passed in.
        """
        if new_value not in self._options_list:
            raise ValueError("{!r} is not in this option menu".format(new_value))
            
        self._var.set(new_value)
        
    def set_index(self, new_idx: int) -> str:
        """
        Set the current value of the option menu to the given index.
        
        :param new_idx: Treated like slice index, so negative values specify indexes
        relative to the right end.
        """
        val = self._options_list[new_idx]
        self.set(val)