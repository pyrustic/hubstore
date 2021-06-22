from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.misc import funcs
import tkinter as tk


class DownloaderView(Viewable):
    def __init__(self, parent_view, owner, repo,
                 release_data, asset_data):
        super().__init__()
        self._parent_view = parent_view
        self._owner = owner
        self._repo = repo
        self._release_data = release_data
        self._asset_data = asset_data
        self._master = parent_view.body
        self._app_name = "{}".format(repo)
        self._body = None
        self._intvar = tk.IntVar()

    def _build(self):
        self._body = tk.Toplevel(self._master)
        self._body.title("Download the latest release")
        self._body.columnconfigure(0, weight=1)
        self._body.rowconfigure(0, weight=0, uniform=1)
        self._body.rowconfigure(1, weight=1, uniform=1)
        self._body.rowconfigure(2, weight=0)

        # information frame
        info_frame = self._gen_information_frame(self._body,
                                                 self._app_name,
                                                 self._release_data)
        info_frame.grid(row=0, column=0, sticky="nswe")

        # asset frame
        if self._asset_data:
            asset_frame = self._gen_asset_frame(self._body,
                                                self._asset_data)
            asset_frame.grid(row=1, column=0, sticky="nswe",
                             pady=5)
        # footer frame
        footer_frame = self._gen_footer_frame(self._body)
        footer_frame.grid(row=2, column=0, sticky="swe")

    def _gen_information_frame(self, master, app_name, release_data):
        frame = tk.Frame(master, name="downloader_information_frame")
        # title
        label_title = tk.Label(frame, name="title_latest_release",
                               text="Latest release", anchor="w")
        label_title.grid(row=0, column=0,
                         columnspan=3,
                         sticky="we",
                         padx=0,
                         pady=(0, 15))
        # == frame application name
        frame_app_name = tk.Frame(frame)
        frame_app_name.grid(row=1, column=0, padx=(2, 5), pady=(0, 7))
        label_app_name = tk.Label(frame_app_name,
                                  text="Application",
                                  anchor="w")
        label_app_name.pack(fill=tk.X)
        entry_app_name = tk.Entry(frame_app_name, width=20)
        entry_app_name.insert(0, app_name)
        entry_app_name.config(state="readonly")
        entry_app_name.pack(fill=tk.X)
        # == frame author name
        frame_author = tk.Frame(frame)
        frame_author.grid(row=2, column=0, padx=(2, 5), pady=(0, 7))
        label_author = tk.Label(frame_author,
                                text="Owner",
                                anchor="w")
        label_author.pack(fill=tk.X)
        entry_author = tk.Entry(frame_author, width=20)
        #entry_author.insert(0, release_data["author_login"])
        entry_author.insert(0, self._owner)
        entry_author.config(state="readonly")
        entry_author.pack(fill=tk.X)
        # == tag name
        frame_tag_name = tk.Frame(frame)
        frame_tag_name.grid(row=1, column=1, padx=(0, 5), pady=(0, 7))
        label_tag_name = tk.Label(frame_tag_name,
                                  text="Tag name",
                                  anchor="w")
        label_tag_name.pack(fill=tk.X)
        entry_tag_name = tk.Entry(frame_tag_name, width=20)
        entry_tag_name.insert(0, release_data["tag_name"])
        entry_tag_name.config(state="readonly")
        entry_tag_name.pack(fill=tk.X)
        # == target comm
        frame_target_comm = tk.Frame(frame)
        frame_target_comm.grid(row=2, column=1, padx=(0, 5), pady=(0, 7))
        label_target_comm = tk.Label(frame_target_comm,
                                     text="Target commitish",
                                     anchor="w")
        label_target_comm.pack(fill=tk.X)
        entry_target_comm = tk.Entry(frame_target_comm, width=20)
        entry_target_comm.insert(0, release_data["target_commitish"])
        entry_target_comm.config(state="readonly")
        entry_target_comm.pack(fill=tk.X)
        # == created at
        frame_created_at = tk.Frame(frame)
        frame_created_at.grid(row=1, column=2, padx=(0, 5), pady=(0, 7))
        label_created_at = tk.Label(frame_created_at,
                                    text="Created at",
                                    anchor="w")
        label_created_at.pack(fill=tk.X)
        entry_created_at = tk.Entry(frame_created_at, width=20)
        entry_created_at.insert(0, release_data["created_at"])
        entry_created_at.config(state="readonly")
        entry_created_at.pack(fill=tk.X)
        # == published at
        frame_published_at = tk.Frame(frame)
        frame_published_at.grid(row=2, column=2, padx=(0, 5), pady=(0, 7))
        label_published_at = tk.Label(frame_published_at,
                                      text="Published at",
                                      anchor="w")
        label_published_at.pack(fill=tk.X)
        entry_published_at = tk.Entry(frame_published_at, width=20)
        entry_published_at.insert(0, release_data["published_at"])
        entry_published_at.config(state="readonly")
        entry_published_at.pack(fill=tk.X)
        return frame

    def _gen_asset_frame(self, master, asset_data):
        frame = tk.Frame(master)
        # title
        text = "Asset{}".format("s" if len(asset_data) > 1 else "")
        label_title = tk.Label(frame, text=text, anchor="w")
        label_title.pack(fill=tk.X, padx=2)
        # scrollbox
        scrollbox = Scrollbox(frame)
        scrollbox.pack(expand=1, fill=tk.BOTH)
        # radio buttons
        for i, asset in enumerate(asset_data):
            asset_frame = tk.Frame(scrollbox.box)
            asset_frame.pack(fill=tk.X, padx=2)
            # radiobutton
            cache = funcs.truncate_str(asset["name"], max_size=42)
            radiobutton = tk.Radiobutton(asset_frame,
                                         variable=self._intvar,
                                         value=i,
                                         text=cache)
            radiobutton.pack(side=tk.LEFT, padx=(0, 15))
            # label size
            entry_size = tk.Label(asset_frame,
                                  text=self._stringify_size(asset["size"]))
            entry_size.pack(side=tk.LEFT, padx=3)
        return frame

    def _gen_footer_frame(self, master):
        frame = tk.Frame(master)
        button_download = tk.Button(frame,
                                    text="Download",
                                    command=self._on_click_download)
        button_download.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        button_cancel = tk.Button(frame,
                                  text="Cancel",
                                  command=self.destroy)
        button_cancel.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        return frame

    def _on_click_download(self):
        if not self._asset_data:
            Toast(self._body, message="No asset to download")
            return
        choice = self._intvar.get()
        name = self._asset_data[choice]["name"]
        url = self._asset_data[choice]["url"]
        self._parent_view.submit_url_to_download(self._owner,
                                                 self._repo,
                                                 name, url)
        self.destroy()

    def _stringify_size(self, data):
        val, unit = funcs.convert_size(data)
        return "{} {}".format(val, unit)
