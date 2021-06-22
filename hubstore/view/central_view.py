import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.view.app_info_view import AppInfoView
from hubstore.misc import my_theme


MAX_TILES_BY_ROW = 4


class CentralView(Viewable):
    def __init__(self, parent_view):
        super().__init__()
        self._parent_view = parent_view
        self._master = self._parent_view.body
        self._host = self._parent_view.main_host
        self._threadom = self._parent_view.threadom
        self._body = None
        self._scrollbox = None
        self._frame_row_cache = None  # will hold: [tk_frame, int_children_count]
        self._image_cache = {}

    @property
    def host(self):
        return self._host

    @property
    def threadom(self):
        return self._threadom

    @property
    def header_view(self):
        return self._parent_view.header_view

    @property
    def footer_view(self):
        return self._parent_view.footer_view

    def load_data(self):
        self._load_data()

    def _build(self):
        self._body = tk.Frame(self._master)
        self._scrollbox = Scrollbox(self._body, orient="v", box_sticky="nswe")
        self._scrollbox.pack(expand=1, fill=tk.BOTH)

    def _load_data(self):
        is_success, error, data = self._host.get_list()
        if not is_success:
            Toast(self._body, message="Failed to load the list of apps")
            return
        self._scrollbox.clear()
        self._frame_row_cache = None
        self._image_cache = {}
        self._loop(data, 0)

    def _loop(self, data, index):
        if index == len(data):
            return
        owner, repo = data[index]
        self._populate(owner, repo)
        index += 1
        command = (lambda self=self, data=data, index=index:
                    self._loop(data, index))
        self._body.after(0, command)

    def _populate(self, owner, host):
        if self._frame_row_cache is None:
            self._add_frame_row()
        elif self._frame_row_cache[1] == MAX_TILES_BY_ROW:
            self._add_frame_row()
        frame_row = self._frame_row_cache[0]
        children_count = self._frame_row_cache[1]
        self._add_tile(frame_row, owner, host)
        self._frame_row_cache[1] = children_count + 1

    def _add_frame_row(self):
        frame = tk.Frame(self._scrollbox.box)
        frame.pack(fill=tk.X)
        self._frame_row_cache = [frame, 0]

    def _add_tile(self, frame_row, owner, repo):
        tile = tk.Frame(frame_row, cursor="hand1")
        tile.pack(side=tk.LEFT, padx=5, pady=5)
        tile.config(highlightthickness=2)
        tile.config(highlightbackground="#101010")
        # owner name
        entry_owner = tk.Entry(tile,borderwidth=0,width=0,
                               name="entry_owner_name",
                               cursor="hand1")
        entry_owner.pack(anchor="center", fill=tk.X,
                         padx=2, pady=(2, 1))
        entry_owner.insert(0, owner)
        entry_owner.config(state="readonly", cursor="hand1")
        entry_owner.bind("<Button-1>", lambda event, tile=tile, self=self:
                            self._on_enter_tile(tile), "+")
        command_entry = (lambda event, self=self, owner=owner, repo=repo:
                        self._on_click_entry(owner, repo))
        # canvas
        command_img = (lambda event,
                              self=self,
                              owner=owner, repo=repo:
                       self._on_click_image(owner, repo))
        canvas = tk.Canvas(tile, width=200, height=80,
                           highlightthickness=0, borderwidth=0)
        canvas.pack(padx=2, pady=1, fill=tk.BOTH, expand=1)
        self._set_image(canvas, owner, repo)
        canvas.bind("<Button-1>", command_img)
        entry_owner.bind("<Button-1>", command_img)
        # repo name
        entry_repo = tk.Entry(tile, borderwidth=0, width=0,
                              name="entry_repo_name",
                              cursor="hand1")
        entry_repo.pack(anchor="w", fill=tk.X,
                        padx=2, pady=(1, 2))
        entry_repo.insert(0, repo)
        entry_repo.config(state="readonly")
        entry_repo.bind("<Button-1>", command_entry)
        entry_repo.bind("<Enter>",
                        lambda event, entry=entry_repo: self._on_enter_repo_name(entry),
                        "+")
        entry_repo.bind("<Leave>",
                        lambda event, entry=entry_repo: self._on_leave_repo_name(entry),
                        "+")
        # bind handlers to canvas event
        canvas.bind("<Enter>",
                  lambda event, tile=tile: self._on_enter_tile(tile), "+")
        canvas.bind("<Leave>",
                  lambda event, tile=tile: self._on_leave_tile(tile), "+")
        # bind handlers to owner name event
        entry_owner.bind("<Enter>",
                    lambda event, tile=tile: self._on_enter_tile(tile), "+")
        entry_owner.bind("<Leave>",
                    lambda event, tile=tile: self._on_leave_tile(tile), "+")

    def _on_click_entry(self, owner, repo):
        footer_view = self.footer_view
        app_info_view = AppInfoView(self, footer_view, owner, repo)
        app_info_view.build()

    def _on_click_image(self, owner, repo):
        target = self._host.run
        footer_view = self._parent_view.footer_view
        args = (owner, repo,
                footer_view.add_item)
        consumer = footer_view.exited_app
        self._threadom.run(target, target_args=args, consumer=consumer)

    def _set_image(self, canvas, owner, repo):
        self.body.update_idletasks()
        data = self._host.get_image(owner, repo)
        if not data:
            return
        image = tk.PhotoImage(data=data)
        #image.zoom(25)
        #image = image.subsample(3, 3)
        self._image_cache["{}/{}".format(owner, repo)] = image
        canvas.create_image(0, 0, image=image, anchor="nw")

    def _on_enter_tile(self, tile):
        tile.config(highlightcolor="#384848")
        tile.config(highlightbackground="#384848")

    def _on_leave_tile(self, tile):
        tile.config(highlightcolor="#101010")
        tile.config(highlightbackground="#102020")
        tile.config(highlightbackground="#101010")

    def _on_enter_repo_name(self, entry):
        hovered_style = my_theme.get_entry_repo_name_hovered_style()
        hovered_style.target(entry, raise_exception=False)

    def _on_leave_repo_name(self, entry):
        default_style = my_theme.get_entry_repo_name_default_style()
        default_style.target(entry, raise_exception=False)
