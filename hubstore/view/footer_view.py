import tkinter as tk
from viewable import Viewable, BUILT, MAPPED
from megawidget.scrollbox import Scrollbox
from hubstore.view.app_info_view import AppInfoView
from hubstore.view.exception_view import ExceptionView


class FooterView(Viewable):
    def __init__(self, parent_view):
        super().__init__()
        self._parent_view = parent_view
        self._master = self._parent_view.body
        self._host = self._parent_view.main_host
        self._threadom = self._parent_view.threadom
        self._body = None
        self._scrollbox = None
        # cache
        self._running_processes = {}
        self._null_frame = None

    @property
    def host(self):
        return self._host

    @property
    def threadom(self):
        return self._threadom

    def add_item(self, owner, repo, process_id):
        if self.state not in (BUILT, MAPPED):
            return
        self._install_item(owner, repo, process_id)
        # scroll to end
        self._scrollbox.xview_moveto(1.0)

    def exited_app(self, data):
        error = data["error"]
        owner = data["owner"]
        repo = data["repo"]
        self._display_error(error, owner, repo)
        process_id = data["id"]
        self._remove_item(process_id)

    def _build(self):
        self._body = tk.Frame(self._master)
        self._scrollbox = Scrollbox(self._body, orient="x", resizable_box=False)
        self._scrollbox.pack(fill=tk.X)

    def _install_item(self, owner, repo, process_id):
        frame = tk.Frame(self._scrollbox.box)
        self._running_processes[process_id] = frame
        frame.pack(side=tk.LEFT, anchor="s",
                   expand=1, fill=tk.BOTH,
                   padx=(1, 15), pady=(5, 10))
        entry_name = tk.Entry(frame,
                              name="entry_running_app_name",
                              cursor="hand1")
        entry_name.pack(side=tk.LEFT, padx=3)
        entry_name.insert(0, repo)
        entry_name.config(state="readonly")
        command = (lambda event, self=self, owner=owner, repo=repo:
                        self._on_click_app_name(owner, repo))
        entry_name.bind("<Button-1>", command)
        command = (lambda self=self, process_id=process_id:
                        self._host.stop_process(process_id))
        button_close = tk.Button(frame, name="button_close", text="x",
                                 command=command)
        button_close.pack(side=tk.LEFT,  padx=(2, 0))

    def _on_click_app_name(self, owner, repo):
        app_info_view = AppInfoView(self, self, owner, repo)
        app_info_view.build()

    def _remove_item(self, process_id):
        if not process_id in self._running_processes:
            return
        frame = self._running_processes[process_id]
        frame.destroy()
        if self._null_frame:
            self._null_frame.destroy()
        self._null_frame = tk.Frame(self._scrollbox.box)
        self._null_frame.pack(side=tk.LEFT)
        del self._running_processes[process_id]

    def _display_error(self, error, owner, repo):
        if not error:
            return
        try:
            error = error.decode()
        except (UnicodeDecodeError, AttributeError):
            pass
        text = "Application: {}/{}\n\n{}".format(owner, repo, error)
        exception_view = ExceptionView(self, text)
        exception_view.build()
