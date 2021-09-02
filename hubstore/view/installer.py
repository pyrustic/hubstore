import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.misc import funcs
from hubstore.misc.theme import get_entry_description_style, \
    get_info_entry_owner_repo_style, get_package_size_style
from cyberpunk_theme.widget.button import get_button_style_4, get_button_style_9


class Installer(Viewable):

    def __init__(self, parent_view, data=None):
        super().__init__()
        self._master = parent_view.body
        self._views = parent_view.views
        self._host = parent_view.host
        self._data = data
        self._strvar_description = tk.StringVar()
        self._strvar_owner_repo = tk.StringVar()
        self._strvar_tag_name = tk.StringVar()
        self._strvar_published_on = tk.StringVar()
        self._strvar_downloads_count = tk.StringVar(value="0")
        self._strvar_package_size = tk.StringVar(value="0 B")
        self._strvar_stargazers = tk.StringVar()
        self._repository_link = None
        self._image_cache = None
        self._asset = None
        self._setup()

    def _build(self):
        self._body = tk.Toplevel(name="installer_toplevel")
        self._body.resizable(False, False)
        #self._body.overrideredirect(1)
        self._body.title("Install an app")
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

    def _setup(self):
        if not self._data:
            return
        self._strvar_owner_repo.set(self._data["owner_repo"])
        self._strvar_description.set(self._data["description"])
        self._strvar_stargazers.set(self._data["stargazers"])
        self._strvar_tag_name.set(self._data["tag"])
        self._strvar_published_on.set(self._data["published_at"])
        self._repository_link = self._data["repository"]
        assets = self._data["assets"]
        if assets:
            self._asset = assets[0]
            self._strvar_downloads_count.set(self._asset["download_count"])
            cache = funcs.convert_size(self._asset["size"])
            self._strvar_package_size.set(cache)

    def _install_header(self):
        # install image
        canvas = tk.Canvas(self._body, width=400, height=100,
                           highlightthickness=0, borderwidth=0,
                           bg="#121519")
        canvas.pack(fill=tk.BOTH, pady=(0, 5))
        data = self._host.data.get_cover_image()
        image = tk.PhotoImage(data=data)
        self._image_cache = image
        canvas.create_image(0, 0, image=image, anchor="nw")
        # description
        description = tk.Entry(self._body,
                               textvariable=self._strvar_description,
                               state="readonly")
        description.pack(fill=tk.X, padx=0)
        get_entry_description_style().target(description)

    def _install_central(self):
        # install identification frame
        self._install_identification_frame()
        # install tag name
        self._install_tag_name()
        # install published_on
        self._install_published_on()
        # install stargazers_count
        self._install_stargazers_count()
        # install downloads_count
        self._install_downloads_count()

    def _install_identification_frame(self):
        # frame
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=(0, 5), pady=5)
        # entry
        entry = tk.Entry(frame, textvariable=self._strvar_owner_repo,
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        get_info_entry_owner_repo_style().target(entry)
        # button
        command = lambda self=self: self._host.open_website(self._repository_link)
        button = tk.Button(frame, text="Repository",
                           command=command)
        button.pack(side=tk.RIGHT)

    def _install_tag_name(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, pady=(0, 5))
        label = tk.Label(frame, text="Tag:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=self._strvar_tag_name,
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        #entry.pack(anchor="w", fill=tk.X, pady=(0, 5))

    def _install_published_on(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, pady=(10, 0))
        label = tk.Label(frame, text="Published:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=self._strvar_published_on,
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        #entry.pack(anchor="w", fill=tk.X, pady=(10, 5))

    def _install_stargazers_count(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, pady=(5, 5))
        label = tk.Label(frame, text="Stargazers:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=self._strvar_stargazers,
                         state="readonly")
        entry.pack(side=tk.LEFT, expand=1, fill=tk.X)

    def _install_downloads_count(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, pady=(0, 5))
        label = tk.Label(frame, text="Downloads:")
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=self._strvar_downloads_count,
                         state="readonly")
        entry.pack(side=tk.LEFT, expand=1, fill=tk.X)
        #entry.pack(anchor="w", fill=tk.X, pady=(0, 5))

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=3, pady=(20, 3))
        # button download
        button_install = tk.Button(frame, text="Install",
                                   command=self._on_click_install)
        button_install.pack(side=tk.RIGHT, padx=(3, 0))
        get_button_style_4().target(button_install)
        # button cancel
        button_cancel = tk.Button(frame, text="Cancel",
                                  command=self.destroy)
        button_cancel.pack(side=tk.RIGHT)
        # package
        entry = tk.Entry(frame, textvariable=self._strvar_package_size,
                         state="readonly")
        entry.pack(side=tk.LEFT, fill=tk.X, anchor="w")
        get_package_size_style().target(entry)

    def _on_click_install(self):
        if not self._asset:
            Toast(self._body, message="No asset to download")
            return
        self.destroy()
        owner, repo = self._data["owner_repo"].split("/")
        name = self._asset["name"]
        url = self._asset["url"]
        self._host.install(owner, repo, name, url)
