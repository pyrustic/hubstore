import tkinter as tk
from viewable import Viewable
from megawidget.scrollbox import Scrollbox
from megawidget.toast import Toast
from hubstore.misc.theme import get_highlight_style, get_unhighlight_style


MAX_TILES_BY_ROW = 4


class Pane(Viewable):
    def __init__(self, parent_view):
        super().__init__()
        self._master = parent_view.body
        self._views = parent_view.views
        self._host = parent_view.host
        self._strvar_title = tk.StringVar()
        self._strvar_notification = tk.StringVar(value="")
        self._frame_matrix = None
        self._frame_row_cache = None  # will hold: [tk_frame, int_children_count]
        self._image_cache = {}
        self._image_cachex = None

    def populate(self, title, data):
        self._strvar_title.set(title)
        self._clear_frame_matrix()
        if not data:
            Toast(self._body, message="No data available")
            return
        self._frame_row_cache = None
        self._image_cache = {}
        self._loop(data, 0)

    def set_notification(self, text=None):
        text = "" if not text else text
        self._strvar_notification.set(text)

    def _build(self):
        self._body = tk.Frame(self._master)
        self._scrollbox = Scrollbox(self._body)
        self._scrollbox.pack(expand=1, fill=tk.BOTH)
        frame_header = tk.Frame(self._scrollbox.box)
        frame_header.pack(fill=tk.X, pady=(10, 1))
        self._frame_matrix = tk.Frame(self._scrollbox.box)
        self._frame_matrix.pack(fill=tk.BOTH, expand=1)
        # label line
        #canvas = tk.Canvas(frame_header, width=43, height=10,
        #                   highlightthickness=0, borderwidth=0)
        #canvas.pack(side=tk.LEFT, padx=0, pady=0)
        #with open("/home/alex/line.png", "rb") as file:
        #    data = file.read()
        #image = tk.PhotoImage(data=data)
        #self._image_cachex = image
        #canvas.create_image(0, 0, image=image, anchor="nw")
        #frame_line = tk.Frame(frame_header, name="frame_line", width=25,
        #                      height=1, pady=0)
        #frame_line.pack(side=tk.LEFT, padx=(2, 3))
        # label title
        label_title = tk.Label(frame_header, name="label_title",
                               textvariable=self._strvar_title)
        label_title.pack(side=tk.LEFT, padx=12)
        # label notification
        label_notification = tk.Label(frame_header, name="label_notification",
                                      textvariable=self._strvar_notification)
        label_notification.pack(side=tk.RIGHT)

    def _on_map(self):
        pass

    def _on_destroy(self):
        pass

    def _loop(self, data, index):
        if index == len(data):
            return
        owner, repo = data[index]
        self._populate(owner, repo)
        index += 1
        command = (lambda self=self, data=data, index=index:
                    self._loop(data, index))
        self._body.after(0, command)

    def _populate(self, owner, repo):
        if self._frame_row_cache is None:
            self._add_frame_row()
        elif self._frame_row_cache[1] == MAX_TILES_BY_ROW:
            self._add_frame_row()
        frame_row = self._frame_row_cache[0]
        children_count = self._frame_row_cache[1]
        self._add_tile(frame_row, owner, repo)
        self._frame_row_cache[1] = children_count + 1

    def _clear_frame_matrix(self):
        if self._frame_matrix:
            self._frame_matrix.destroy()
        self._frame_matrix = tk.Frame(self._scrollbox.box)
        self._frame_matrix.pack(fill=tk.BOTH, expand=1)

    def _add_frame_row(self):
        frame = tk.Frame(self._frame_matrix)
        frame.pack(fill=tk.X, padx=5)
        self._frame_row_cache = [frame, 0]

    def _add_tile(self, frame_row, owner, repo):
        tile = tk.Frame(frame_row)
        tile.pack(side=tk.LEFT, padx=5, pady=(0, 10))
        #tile.config(highlightthickness=2)
        #tile.config(highlightbackground="white")
        get_unhighlight_style().target(tile)
        # owner name
        entry_owner = tk.Entry(tile,borderwidth=0,width=0,
                               name="entry_owner_name",
                               cursor="hand1")
        entry_owner.pack(anchor="center", fill=tk.X,
                         padx=2, pady=(2, 1))
        entry_owner.insert(0, owner)
        entry_owner.config(state="readonly", cursor="hand1")
        # canvas
        canvas = tk.Canvas(tile, width=200, height=80,
                           highlightthickness=0, borderwidth=0,
                           cursor="hand1")
        canvas.pack(padx=2, pady=1, fill=tk.BOTH, expand=1)
        self._set_image(canvas, owner, repo)
        # repo name
        entry_repo = tk.Entry(tile, borderwidth=0, width=0,
                              name="entry_repo_name",
                              cursor="hand1")
        entry_repo.pack(anchor="w", fill=tk.X,
                        padx=2, pady=(0, 2), ipady=2)
        entry_repo.insert(0, repo)
        entry_repo.config(state="readonly")
        # binding
        self._bind_handler_owner(owner, tile, entry_owner)
        self._bind_handler_canvas(owner, repo, tile, canvas)
        self._bind_handler_repo(owner, repo, tile, entry_repo)

    def _set_image(self, canvas, owner, repo):
        self.body.update_idletasks()
        data = self._host.data.get_image(owner, repo)
        if not data:
            return
        image = tk.PhotoImage(data=data)
        #image.zoom(25)
        #image = image.subsample(3, 3)
        self._image_cache["{}/{}".format(owner, repo)] = image
        canvas.create_image(0, 0, image=image, anchor="nw")

    def _bind_handler_owner(self, owner, tile, entry_owner):
        # on click
        command = (lambda event, self=self, owner=owner:
                   self._on_click_owner(owner))
        entry_owner.bind("<Button-1>", command, "+")
        # on enter
        command = (lambda event, tile=tile:
                   get_unhighlight_style().target(tile))
        entry_owner.bind("<Enter>", command, "+")
        # on leave
        entry_owner.bind("<Leave>", command, "+")

    def _bind_handler_canvas(self, owner, repo, tile, canvas):
        # handle Click on Canvas
        command = (lambda event, self=self, owner=owner,
                          repo=repo:
                   self._on_click_canvas(owner, repo))
        canvas.bind("<Button-1>", command)
        # handle on enter Canvas
        command = (lambda event, tile=tile:
                   get_highlight_style().target(tile))
        canvas.bind("<Enter>", command, "+")
        # handle on leave Canvas
        command = (lambda event, tile=tile:
                   get_unhighlight_style().target(tile))
        canvas.bind("<Leave>", command, "+")

    def _bind_handler_repo(self, owner, repo, tile, entry_repo):
        command_entry = (lambda event, self=self, owner=owner, repo=repo:
                         self._on_click_repo(owner, repo))
        # on click
        entry_repo.bind("<Button-1>", command_entry)
        # on enter
        command = (lambda event, tile=tile:
                   get_unhighlight_style().target(tile))
        entry_repo.bind("<Enter>", command, "+")
        # on leave
        entry_repo.bind("<Leave>", command, "+")

    def _on_click_owner(self, owner):
        self._host.show_apps_from(owner)

    def _on_click_canvas(self, owner, repo):
        self._host.run_app(owner, repo)

    def _on_click_repo(self, owner, repo):
        self._host.show_app_info(owner, repo)


    """
    def _on_click_entry(self, owner, repo):
        print("on_click_entry", owner, repo)
        return
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

    def _on_enter_tile(self, tile):
        tile.config(highlightcolor="#384848")
        tile.config(highlightbackground="#384848")

    def _on_leave_tile(self, tile):
        tile.config(highlightcolor="#101010")
        tile.config(highlightbackground="#102020")
        tile.config(highlightbackground="#101010")

    def _on_enter_repo_name(self, entry):
        print("on_enter_repo_name", entry)
        return
        hovered_style = my_theme.get_entry_repo_name_hovered_style()
        hovered_style.target(entry, raise_exception=False)

    def _on_leave_repo_name(self, entry):
        print("on_leave_repo_name", entry)
        return
        default_style = my_theme.get_entry_repo_name_default_style()
        default_style.target(entry, raise_exception=False)
    
    """
