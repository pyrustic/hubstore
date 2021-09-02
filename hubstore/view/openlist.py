import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.misc.theme import get_entry_description_style, \
    get_info_entry_owner_repo_style, get_package_size_style
from cyberpunk_theme.widget.button import get_button_style_4, get_button_style_9


class Openlist(Viewable):

    def __init__(self, parent_view, data=None):
        super().__init__()
        self._data = data
        self._master = parent_view.body
        self._views = parent_view.views
        self._host = parent_view.host
        self._strvar_description = tk.StringVar(value="Currently running")
        self._strvar_owner_repo = tk.StringVar(value="pyrustic/demo")
        self._strvar_tag_name = tk.StringVar(value="v10.0.2")
        self._strvar_published_on = tk.StringVar(value="January 21, 2021 at 12:20 UTC")
        self._strvar_created_on = tk.StringVar(value="March 14, 2021 at 09:10 UTC")
        self._strvar_stargazers_count = tk.StringVar(value="34")
        self._strvar_downloads_count = tk.StringVar(value="345")
        self._strvar_package_size = tk.StringVar(value="24 KB")
        self._image_cache = None
        self._scrollbox = None

    def _build(self):
        self._body = tk.Toplevel(name="openlist_toplevel")
        self._body.geometry("350x250")
        self._body.title("Apps Manager")
        self._body.resizable(False, False)
        #self._body.overrideredirect(1)
        self._scrollbox = Scrollbox(self._body)
        self._scrollbox.pack(expand=1, fill=tk.BOTH)
        # install header
        self._install_header()
        # install central
        self._install_central()
        # install footer
        self._install_footer()

    def _on_map(self):
        super()._on_map()

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
        description = tk.Label(self._scrollbox.box, font=("Liberation Mono", 11, "bold"),
                               textvariable=self._strvar_description)
        description.pack(pady=(10, 10), anchor="center")
        #get_entry_description_style().target(description)

    def _install_central(self):
        # install identification frame
        for item in self._data:
            owner = item["owner"]
            repo = item["repo"]
            process_id = item["id"]
            self._install_identification_frame(owner, repo, process_id)

    def _install_identification_frame(self, owner, repo, process_id):
        # frame
        frame = tk.Frame(self._scrollbox.box)
        frame.pack(fill=tk.X, padx=(3, 5), pady=5)
        # entry
        owner_repo = "{}/{}".format(owner, repo)
        strvar = tk.StringVar(value=owner_repo)
        entry = tk.Entry(frame, textvariable=strvar,
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        #get_info_entry_owner_repo_style().target(entry)
        # button
        command = (lambda self=self, frame=frame,
                          process_id=process_id:
                   self._on_close_app(frame, process_id))
        button = tk.Button(frame, text="Stop",
                           command=command)
        button.pack(side=tk.LEFT, padx=(5, 0))
        get_button_style_9().target(button)

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=(15, 3))
        # button close
        button = tk.Button(frame, text="Close",
                           command=self.destroy)
        button.pack(side=tk.RIGHT)

    def _on_close_app(self, frame, process_id):
        self._host.close_app(process_id)
        frame.destroy()
