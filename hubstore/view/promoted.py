import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.misc.theme import get_entry_description_style, \
    get_info_entry_owner_repo_style, get_package_size_style
from cyberpunk_theme.widget.button import get_button_style_1, get_button_style_4, get_button_style_7


class Promoted(Viewable):

    def __init__(self, parent_view, data=None):
        super().__init__()
        self._data = data
        self._master = parent_view.body
        self._views = parent_view.views
        self._host = parent_view.host
        self._image_cache = None
        self._scrollbox = None

    def _build(self):
        self._body = tk.Toplevel(name="promoted_toplevel")
        self._body.geometry("380x250")
        self._body.title("Promoted Apps")
        self._body.resizable(False, False)
        #self._body.overrideredirect(1)
        self._scrollbox = Scrollbox(self._body)
        self._scrollbox.pack(expand=1, fill=tk.BOTH)
        # install header
        #self._install_header()
        # install central
        self._install_central()
        # install footer
        self._install_footer()

    def _on_map(self):
        super()._on_map()
        if not self._data:
            self._body.destroy()
            Toast(message="Nothing to show !",
                  duration=1000)

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
                               text="These are promoted apps")
        description.pack(pady=(10, 10), anchor="center")
        #get_entry_description_style().target(description)

    def _install_central(self):
        # install
        for item in self._data:
            owner_repo = item["repository"]
            description = item["description"]
            github_prefix = "https://github.com/"
            if owner_repo.startswith(github_prefix):
                owner_repo = owner_repo.lstrip(github_prefix)
            self._install_row(owner_repo, description)

    def _install_row(self, owner_repo, description):
        # frame
        frame = tk.Frame(self._scrollbox.box)
        frame.pack(fill=tk.X, padx=(3, 5), pady=10)
        # description
        strvar_description = tk.StringVar(value=description)
        description = tk.Entry(frame,
                               textvariable=strvar_description,
                               state="readonly")
        description.pack(fill=tk.X, padx=2)
        get_entry_description_style().target(description)
        # subframe
        subframe = tk.Frame(frame)
        subframe.pack(fill=tk.X)
        # entry
        strvar_owner_repo = tk.StringVar(value=owner_repo)
        entry = tk.Entry(subframe, textvariable=strvar_owner_repo,
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        get_info_entry_owner_repo_style().target(entry)
        # button get
        command = (lambda self=self, owner_repo=owner_repo:
                   self._on_click_get(owner_repo))
        button_get = tk.Button(subframe, text="Get",
                           command=command)
        button_get.pack(side=tk.LEFT, padx=(5, 0))
        # button visit
        command = (lambda self=self, owner_repo=owner_repo:
                   self._on_click_visit(owner_repo))
        button_visit = tk.Button(subframe, text="Visit",
                               command=command)
        button_visit.pack(side=tk.LEFT, padx=(5, 0))

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=(15, 3))
        # button close
        button_more = tk.Button(frame, text="More",
                           command=self._on_click_more)
        button_more.pack(side=tk.RIGHT, padx=(3, 0))
        # button more
        button_close = tk.Button(frame, text="Close",
                           command=self.destroy)
        button_close.pack(side=tk.RIGHT)
        get_button_style_4().target(button_more)

    def _on_click_get(self, owner_repo):
        cache = owner_repo.split("/")
        if len(cache) != 2:
            return
        owner, repo = cache
        self._host.search(owner, repo)
        self.destroy()

    def _on_click_visit(self, owner_repo):
        github_prefix = "https://github.com/"
        repository = "{}{}".format(github_prefix, owner_repo)
        self._host.open_website(repository)


    def _on_click_more(self):
        self.destroy()
        self._host.show_promoted()
