import tkinter as tk
from viewable import Viewable


class ExceptionView(Viewable):
    def __init__(self, parent_view, data):
        super().__init__()
        self._parent_view = parent_view
        self._data = data
        self._master = parent_view.body
        self._body = None

    def _build(self):
        self._body = tk.Toplevel(self._master, name="exception_view")
        self._body.title("Oops ! An Exception occurred !")
        text = tk.Text(self._body, width=50,
                       height=20,
                       wrap="word")
        text.insert("1.0", self._data)
        text.pack(fill=tk.BOTH, expand=1)
        text.config(state="disabled")
        button_close = tk.Button(self._body,
                                 text="Close",
                                 command=self.destroy)
        button_close.pack(anchor="e", padx=2, pady=(7, 2))
