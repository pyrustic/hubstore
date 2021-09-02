import tkinter as tk
from viewable import Viewable
from megawidget.pathentry import Pathentry
import os
import os.path
from cyberpunk_theme.widget.button import get_button_style_4, get_button_style_7


ABOUT_TEXT = """Download, install, manage, promote, and run Python desktop apps with Hubstore.

Hubstore is part of the Pyrustic Open Ecosystem.

"""


WEBSITE = "https://pyrustic.github.io"


class About(Viewable):
    def __init__(self, parent_view):
        super().__init__()
        self._app = parent_view.app
        self._master = parent_view.body
        self._host = parent_view.host
        self._strvar_apps_directory = tk.StringVar(value="")

    @property
    def directory_path(self):
        return self._strvar_apps_directory.get()

    def _build(self):
        self._body = tk.Toplevel(self._master)
        self._body.title("About Hubstore")
        self._body.resizable(False, False)
        # install header
        self._install_header()
        # install central
        self._install_central()
        # install directory form
        self._install_directory_form()
        # install footer
        self._install_footer()

    def _on_map(self):
        super()._on_map()
        apps_directory = self._host.data.get_apps_directory()
        self._strvar_apps_directory.set(apps_directory)

    def _on_destroy(self):
        pass

    def _install_header(self):
        # install image
        canvas = tk.Canvas(self._body, width=400, height=100,
                           highlightthickness=0, borderwidth=0,
                           bg="#121519")
        canvas.pack(fill=tk.BOTH, pady=(0,5))
        data = self._host.data.get_cover_image()
        image = tk.PhotoImage(data=data)
        self._image_cache = image
        canvas.create_image(0, 0, image=image, anchor="nw")
        label = tk.Label(self._body, text="H U B S T O R E", fg="#4E7F7A",
                         font=("Liberation Mono", 25, "bold"))
        label.pack(anchor="center")

    def _install_central(self):
        # text
        text = tk.Text(self._body, width=1, height=6, bg="#121519",
                       fg="gray", font=("Liberation Mono", 12, "normal"),
                       wrap="word", borderwidth=0, highlightthickness=0)
        text.insert("1.0", ABOUT_TEXT)
        text.config(state="disabled")
        text.pack(fill=tk.X, pady=10, padx=3, expand=1)

    def _install_directory_form(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=(0, 20))
        label = tk.Label(frame, text="Directory to store apps", padx=0, borderwidth=0)
        label.pack(anchor="w")
        pathentry = Pathentry(frame, browse="dir",
                              initialdir=os.path.expanduser("~"),
                              textvariable=self._strvar_apps_directory)
        pathentry.pack(fill=tk.X, anchor="w")

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=3)
        command = lambda self=self: self._on_click_website()
        button_website = tk.Button(frame, text="Website", command=command)
        button_website.pack(side=tk.LEFT, padx=(0, 3))
        get_button_style_7().target(button_website)
        command = lambda self=self: self._on_click_accept()
        button_accept = tk.Button(frame, text="Accept", command=command)
        button_accept.pack(side=tk.RIGHT)
        get_button_style_4().target(button_accept)
        command = lambda self=self: self.destroy()
        button_close = tk.Button(frame, text="Close", command=command)
        button_close.pack(side=tk.RIGHT, padx=3)

    def _on_click_accept(self):
        self._host.submit_apps_directory(self._strvar_apps_directory.get())
        self.destroy()

    def _on_click_website(self):
        self._host.open_website(WEBSITE)
