import tkinter as tk
from viewable import Viewable
from suggestion import Suggestion, Engine
from hubstore.misc.constant import SPECIAL_COMMANDS
from hubstore.misc.theme import get_text_search_style


class Toolbar(Viewable):
    def __init__(self, master, views, host):
        super().__init__()
        self._master = master
        self._views = views
        self._host = host
        self._entry_search = None
        self._search_strvar = tk.StringVar()
        self._open_count = tk.StringVar(value="0 Open")
        self._button_all = None
        self._button_favorites = None
        self._button_promoted = None
        self._button_open = None
        self._button_issues = None
        self._suggestion_engine = None

    def wake_search_entry(self):
        self._entry_search.focus_set()

    def update_open_count(self, count):
        text = "{} Open"
        cache = "99+"
        if count < 100:
            cache = str(count)
        text = text.format(cache)
        self._open_count.set(text)

    def update_apps_list(self, apps_list):
        self._suggestion_engine.owners_repos = apps_list

    def _on_search(self):
        search = self._search_strvar.get()
        github_prefix = "https://github.com/"
        if search.startswith(github_prefix):
            search = search.lstrip(github_prefix)
        self._search_strvar.set("")
        if search.startswith("@"):
            cache = search.split(":")
            if len(cache) != 2:
                return
            command, query = cache
        else:
            command = "@search"
            query = search
        self._interpret_query(command, query)

    def _on_click_all(self):
        self._host.show_all_apps()

    def _on_click_favorites(self):
        self._host.show_favorite_apps()

    def _on_click_promoted(self):
        self._host.show_promoted()

    def _on_click_open(self):
        self._host.show_open()

    def _on_click_about(self):
        self._host.show_about()

    def _interpret_query(self, command, query):
        if not query:
            return
        if command == "@from":
            self._host.show_apps_from(query)
            return
        cache = query.split("/")
        if len(cache) != 2:
            return
        owner, repo = cache
        if command == "@run":
            self._host.run_app(owner, repo)
        else:  # search
            self._host.search(owner, repo)

    def _build(self):
        self._body = tk.Frame(self._master)
        # install search field
        self._install_search_field()
        # install buttons
        self._install_buttons()

    def _on_map(self):
        self._link_suggestion()
        self._entry_search.bind("<Return>",
                                lambda e, self=self: self._on_search(), "+")

    def _on_destroy(self):
        pass

    def _install_search_field(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, side=tk.LEFT, expand=1)
        # Search:
        strvar = tk.StringVar(value="Search:")
        entry = tk.Entry(frame, width=7, textvariable=strvar,
                         state="readonly", cursor="hand1")
        entry.pack(side=tk.LEFT)
        entry.bind("<Button-1>", lambda e, self=self: self._on_search())
        get_text_search_style().target(entry)
        # search entry
        self._entry_search = tk.Entry(frame,
                                      textvariable=self._search_strvar)
        self._entry_search.pack(side=tk.LEFT, fill=tk.X,
                                expand=1, padx=(0, 5), anchor="center")

    def _install_buttons(self):
        # button All
        self._button_all = tk.Button(self._body, text="All",
                                     command=self._on_click_all)
        self._button_all.pack(side=tk.LEFT, padx=(0, 5))
        # button Favorites
        self._button_favorites = tk.Button(self._body, text="Favorites",
                                     command=self._on_click_favorites)
        self._button_favorites.pack(side=tk.LEFT, padx=(0, 5))
        # button Promoted
        self._button_promoted = tk.Button(self._body, text="Promoted",
                                          command=self._on_click_promoted)
        self._button_promoted.pack(side=tk.LEFT, padx=(0, 5))
        # button Open
        self._button_open = tk.Button(self._body, textvariable=self._open_count,
                                          command=self._on_click_open)
        self._button_open.pack(side=tk.LEFT, padx=(0, 5))
        # button About
        command = lambda self=self: self._host.show_about()
        button_about = tk.Button(self._body, text="About",
                                 command=self._on_click_about)
        button_about.pack(side=tk.LEFT)

    def _link_suggestion(self):
        suggestion = Suggestion(self._entry_search)
        self._suggestion_engine = SuggestionEngine(suggestion,
                                                   commands=SPECIAL_COMMANDS)
        suggestion.engine = self._suggestion_engine


class SuggestionEngine(Engine):
    def __init__(self, suggestion, commands=None, owners_repos=None):
        self._suggestion = suggestion
        self._owners_repos = None
        self._owners = None
        self._commands = None
        self._prepare_dataset(commands=commands,
                              owners_repos=owners_repos)
        self._setup()

    @property
    def owners_repos(self):
        return self._owners_repos

    @owners_repos.setter
    def owners_repos(self, val):
        self._prepare_dataset(owners_repos=val)

    def process(self, info, callback):
        if info.special_word:
            return
        word = info.word
        if word.startswith("@"):
            cache = self._basic_search(word, self._commands)
            callback(cache)
            return
        if info.cached_word == "@from:":
            cache = self._basic_search(word, self._owners)
            callback(cache)
            return
        cache = []
        for owner, repo in self._owners_repos:
            if word in owner or word in repo:
                cache.append("{}/{}".format(owner, repo))
        callback(cache)

    def _setup(self):
        self._owners_repos = (self._owners_repos if self._owners_repos
                              else ())
        self._owners = (self._owners if self._owners
                        else ())

    def _basic_search(self, word, dataset):
        cache = []
        for item in dataset:
            if word in item:
                cache.append(item)
        return cache

    def _prepare_dataset(self, commands=None, owners_repos=None):
        if commands is not None:
            self._commands = ["@{}: ".format(command)
                              for command in commands]
        if owners_repos is not None:
            self._owners_repos = owners_repos
            self._owners = [owner for owner, repo in owners_repos]


class Dataset:
    def __init__(self):
        self.owners_repos = None
        self.commands = None
