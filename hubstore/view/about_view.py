import tkinter as tk
from viewable import Viewable
import webbrowser


ABOUT_TEXT = """Download, install, manage, and run Python desktop apps with Hubstore.
Hubstore is available on PyPI and is built with Pyrustic.

Hubstore web page:
https://github.com/pyrustic/hubstore

Pyrustic web page:
https://github.com/pyrustic/pyrustic


To install Hubstore:
pip install hubstore

To upgrade Hubstore:
pip install hubstore --upgrade --upgrade-strategy eager


"""
HUBSTORE_URL = "https://github.com/pyrustic/hubstore#readme"
PYRUSTIC_URL = "https://github.com/pyrustic/pyrustic#readme"


class AboutView(Viewable):
    def __init__(self, parent_view):
        super().__init__()
        self._parent_view = parent_view
        self._master = self._parent_view.body
        self._body = None

    def _build(self):
        self._body = tk.Toplevel(self._master, name="about_view")
        self._body.title("About | Hubstore")
        # text
        text = tk.Text(self._body, width=70, height=20)
        text.insert("1.0", ABOUT_TEXT)
        text.config(state="disabled")
        text.pack(fill=tk.X)
        # footer
        footer_frame = tk.Frame(self._body)
        footer_frame.pack(fill=tk.X)
        # button open hubstore web page
        button_open_hubstore = tk.Button(footer_frame,
                                 text="Visit Hubstore web page",
                                 command=self._on_click_open_hubstore)
        button_open_hubstore.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        # button open pyrustic web page
        button_open_pyrustic = tk.Button(footer_frame,
                                         text="Visit Pyrustic web page",
                                         command=self._on_click_open_pyrustic)
        button_open_pyrustic.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        # button close
        button_close = tk.Button(footer_frame,
                                 text="Cancel",
                                 command=self.destroy)
        button_close.pack(side=tk.RIGHT, padx=(0, 2), pady=2)

    def _on_destroy(self):
        pass

    def _on_click_open_hubstore(self):
        webbrowser.open(HUBSTORE_URL, new=2)

    def _on_click_open_pyrustic(self):
        webbrowser.open(PYRUSTIC_URL, new=2)
