import os.path
import tkinter as tk
from tkinter import filedialog
from pyrustic.view import View
from pyrustic.widget.toast import Toast
from pyrustic import tkmisc


class InitGeetView(View):
    def __init__(self, parent_view):
        super().__init__()
        self._parent_view = parent_view
        self._master = parent_view.body
        self._host = parent_view.main_host
        self._threadom = parent_view.threadom
        self._central_view = parent_view.central_view
        self._body = None
        self._strvar_path = tk.StringVar()
        self._entry_path = None
        self._init_success = False

    def notify_init_outcome(self, data):
        error_code = data["error_code"]
        message = "Thanks you and Welcome !"
        if error_code == 0:
            self._init_success = True
            toast = Toast(self._body, message=message)
            toast.wait_window()
            self._central_view.load_data()
            self.destroy()
            return
        cache = {1: "Failed to create 'got-with-geet' folder",
                 2: "Failed to register Geet in $HOME/PyrusticData"}
        message = cache[error_code]
        toast = Toast(self._body, message=message)
        toast.wait_window()

    def _on_build(self):
        self._body = tk.Toplevel(self._master, name="init_geet_view")
        self._body.resizable(0, 0)
        # Label Title
        label_title = tk.Label(self._body, name="init_geet_label",
                               text="Initialization", anchor="w")
        label_title.pack(anchor="w", fill=tk.X)
        # Text description
        text_description = tk.Text(self._body, wrap="word",
                                   width=50, height=10)
        message = "\nHubstore needs a directory to install apps inside.\n\n"
        message += "A folder named 'hubstore-apps' "
        message += "will be created in the directory that you will submit.\n"
        message += "\nSubmit a path to initialize Hubstore."
        text_description.insert("0.0", message)
        text_description.pack(expand=1, fill=tk.BOTH)
        # Label 'Path'
        label_path = tk.Label(self._body, text="Path")
        label_path.pack(anchor="w", pady=(5, 0))
        # frame entry and three_dot_button
        frame_for_path = tk.Frame(self._body)
        frame_for_path.pack(fill=tk.X, pady=(0, 10))
        # entry
        self._entry_path = tk.Entry(frame_for_path,
                         textvariable=self._strvar_path)
        self._entry_path.pack(side=tk.LEFT,
                   expand=1,
                   fill=tk.X, padx=2)
        self._entry_path.focus_set()
        # three_dot_button
        button = tk.Button(frame_for_path,
                           text="...",
                           command=self._on_click_three_dot)
        button.pack(side=tk.RIGHT, padx=(0, 2))
        # frame footer
        frame_footer = tk.Frame(self._body)
        frame_footer.pack(fill=tk.X)
        # button init
        button_init = tk.Button(frame_footer,
                                text="Init",
                                command=self._on_click_init)
        button_init.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        # button cancel
        button_cancel = tk.Button(frame_footer,
                                  text="Cancel",
                                  command=self.destroy)
        button_cancel.pack(side=tk.RIGHT, padx=(0, 2), pady=2)

    def _on_display(self):
        pass

    def _on_destroy(self):
        if not self._init_success:
            self._parent_view.leave()

    def _toplevel_geometry(self):
        super()._toplevel_geometry()
        tkmisc.dialog_effect(self._body)

    def _on_click_three_dot(self):
        path = self._get_path()
        if path is None:
            return
        self._strvar_path.set(path)
        self._entry_path.icursor("end")

    def _on_click_init(self):
        path = self._strvar_path.get()
        if path and os.path.isdir(path):
            target = self._host.init_hubstore
            args = (path, )
            consumer = self.notify_init_outcome
            self._threadom.run(target, target_args=args, consumer=consumer)
            return
        message = ("Please set a path !" if path == ""
                   else "This path doesn't exist !")
        toast = Toast(self._body, message=message)
        toast.build()

    def _get_path(self):
        initialdir = os.path.expanduser("~")
        path = filedialog.askdirectory(initialdir=initialdir,
                                       title="Select a folder")
        if not isinstance(path, str) or not path:
            return None
        return path
