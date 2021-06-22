import tkinter as tk
from viewable import Viewable
from megawidget.toast import Toast
from megawidget.scrollbox import Scrollbox


class ImportListView(Viewable):
    def __init__(self, parent_view, header_view, data):
        super().__init__()
        self._parent_view = parent_view
        self._header_view = header_view
        self._data = data
        self._host = parent_view.host
        self._threadom = parent_view.threadom
        self._master = parent_view.body
        self._intvar = tk.IntVar(value=0)
        self._index = 0
        self._toast_cache = None

    def notify_online_search_result(self, owner, repo, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        self._header_view.notify_online_search_result(owner, repo, result)

    def _build(self):
        self._body = tk.Toplevel()
        self._body.resizable(False, False)
        self._body.rowconfigure(0, weight=0, uniform="a")
        self._body.rowconfigure(1, weight=7, uniform="a")
        message = "Select an app to download"
        label = tk.Label(self._body, text=message)
        label.grid(row=0, column=0, sticky="we",
                   padx=(2, 50), pady=(5, 10))
        scrollbox = Scrollbox(self._body)
        scrollbox.grid(row=1, column=0,
                             sticky="nswe")
        for i, owner_repo in enumerate(self._data):
            radiobutton = tk.Radiobutton(scrollbox.box,
                                         text=owner_repo,
                                         variable=self._intvar,
                                         value=i)
            radiobutton.pack(anchor="w")
        footer = tk.Frame(self._body)
        footer.grid(row=2, column=0,
                    pady=(10, 0), sticky="we")
        button_download = tk.Button(footer,
                                    text="Download",
                                    command=self._on_click_download)
        button_download.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        button_cancel = tk.Button(footer,
                                  text="Cancel",
                                  command=self.destroy)
        button_cancel.pack(side=tk.RIGHT, padx=(0, 2), pady=2)

    def _on_click_download(self):
        user_choice = self._intvar.get()
        text = self._data[user_choice]
        if user_choice < (len(self._data) - 1):
            user_choice += 1
            self._intvar.set(user_choice)
        owner, repo = self._host.parse_owner_repo(text)
        if owner is None:
            return
        self._toast_cache = Toast(self._body,
                                  message="Fetching...",
                                  duration=None)
        host = self._host.search_online
        args = (owner, repo)
        consumer = (lambda result,
                           self=self,
                           owner=owner,
                           repo=repo:
                    self.notify_online_search_result(owner, repo, result))
        self._threadom.run(host,
                           target_args=args,
                           consumer=consumer,
                           sync=True)
