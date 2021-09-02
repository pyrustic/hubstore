import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.misc.theme import get_entry_description_style, \
    get_info_entry_owner_repo_style, get_package_size_style
from cyberpunk_theme.widget.button import get_button_style_4, get_button_style_9


class Report(Viewable):

    def __init__(self, parent_view, data=None):
        super().__init__()
        self._master = parent_view.body
        self._views = parent_view.views
        self._host = parent_view.host
        self._data = data
        self._strvar_description = tk.StringVar(value="Oops, an error occurred !")
        self._strvar_owner_repo = tk.StringVar()
        self._text_widget = None
        self._image_cache = None
        self._scrollbox = None
        self._setup()

    def _build(self):
        self._body = tk.Toplevel(name="error_toplevel")
        self._body.resizable(False, False)
        self._body.title("Crash report")
        #self._body.geometry("350x250")
        #self._body.overrideredirect(1)
        # install header
        self._install_header()
        # install central
        self._install_central()
        # install footer
        self._install_footer()

    def _on_map(self):
        super()._on_map()
        self._strvar_owner_repo.set(self._data["owner_repo"])
        self._text_widget.insert("1.0", self._data["error"])
        self._text_widget.config(state="disabled")

    def _on_destroy(self):
        pass

    def _install_header(self):
        """
        # install image
        canvas = tk.Canvas(self._body, width=400, height=100,
                           highlightthickness=0, borderwidth=0,
                           bg="#121519")
        canvas.pack(fill=tk.BOTH, pady=(0,5))
        with open("/home/alex/default_info_cover.png",
                  "rb") as file:
            data = file.read()
        image = tk.PhotoImage(data=data)
        self._image_cache = image
        canvas.create_image(0, 0, image=image, anchor="nw")
        """
        # description
        description = tk.Label(self._body,
                               textvariable=self._strvar_description)
        description.pack(pady=(10, 10), anchor="center")
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, expand=1)
        label = tk.Label(frame, text="Application:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=self._strvar_owner_repo,
                         state="readonly")
        entry.pack(side=tk.LEFT, expand=1, fill=tk.X)
        #get_entry_description_style().target(description)

    def _install_central(self):
        # install identification frame
        self._text_widget = ScrolledText(self._body, width=52, height=13,
                                         wrap="word")
        self._text_widget.pack(pady=10)

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=(15, 3))
        # button report
        button_report = tk.Button(frame, text="Report",
                                  command=self._on_click_report)
        button_report.pack(side=tk.RIGHT)
        get_button_style_4().target(button_report)
        # button copy
        button_copy = tk.Button(frame, text="Copy",
                                command=self._on_click_copy)
        button_copy.pack(side=tk.RIGHT, padx=(0, 3))
        # button close
        button_close = tk.Button(frame, text="Close",
                                 command=self.destroy)
        button_close.pack(side=tk.RIGHT, padx=(0, 3))

    def _setup(self):
        """
        self._data =  {"error": error, "owner_repo": owner_repo,
                    "repository": repository}
        """
        pass

    def _on_click_copy(self):
        self._body.clipboard_clear()
        text = self._data["error"]
        self._body.clipboard_append(text)
        self._body.update()
        Toast(self._body, message="Traceback copied !", duration=700)

    def _on_click_report(self):
        self._host.open_website(self._data["repository"])
