import os
import os.path
import tkinter as tk
from tkinter import filedialog
from viewable import Viewable
from megawidget.toast import Toast
from hubstore.view.downloader_view import DownloaderView
from hubstore.view.about_view import AboutView
from hubstore.view.auth_view import AuthView
from hubstore.view.app_info_view import AppInfoView
from hubstore.view.import_list_view import ImportListView
from hubstore.misc import funcs


class HeaderView(Viewable):

    def __init__(self, parent_view):
        super().__init__()
        self._parent_view = parent_view
        self._threadom = self._parent_view.threadom
        self._master = self._parent_view.body
        self._host = self._parent_view.main_host
        self._body = None
        self._strvar_search = tk.StringVar()
        self._toast_cache = None
        self._button_auth = None

    @property
    def host(self):
        return self._host

    @property
    def central_view(self):
        return self._parent_view.central_view

    @property
    def threadom(self):
        return self._threadom

    # =====================
    #       PUBLIC
    # =====================
    def notify_offline_search_result(self, owner, repo, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        if result:
            self._open_app_info(owner, repo)
        else:
            self._request_an_online_search(owner, repo)

    def notify_online_search_result(self, owner, repo, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        success = result["success"]
        status = result["status"]
        if not success:
            message = "Failed to fetch data\n{} {}".format(status[0], status[1])
            Toast(self._body, message=message)
        else:
            downloader_view = DownloaderView(self,
                                             owner, repo,
                                             result["release"],
                                             result["assets"])
            downloader_view.build()

    def notify_download(self, owner, repo, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        success = result["success"]
        message = "Failed to download\n{}".format(result["error"])
        if result["success"]:
            message = "Successfully downloaded"
        Toast(self._body, message=message)
        if success:
            self._parent_view.central_view.load_data()

    def notify_rate(self, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        status_code = result["status_code"]
        status_text = result["status_text"]
        data = result["data"]
        message = None
        duration = 5000
        if status_code in (200, 304):
            message = "Rate Limit:\t{}\nRemaining :\t{}".format(data["limit"],
                                                                data["remaining"])
            message = funcs.tab_to_space(message, tab_size=4)
        else:
            duration = 1000
            message = "Failed to load data\n{}".format(status_text)
        Toast(self._body, message=message, duration=duration)

    def notify_list(self, result):
        is_success, error, data = result
        if not is_success:
            Toast(self._body, message="Failed to load data").wait_window()
            return
        cache = os.path.expanduser("~")
        filename = filedialog.asksaveasfilename(initialdir=cache,
                                                title="Export the list of apps")
        if not isinstance(filename, str) or not filename:
            return
        if os.path.exists(filename):
            os.unlink(filename)
        self._save_apps_list_in_file(data, filename)
        message = "Successfully exported !\n{}".format(filename)
        Toast(self.body, message=message)

    def submit_url_to_download(self, owner, repo, name, url):
        if self._toast_cache:
            self._toast_cache.destroy()
        self._toast_cache = Toast(self._body,
                                  message="Processing...",
                                  duration=None)
        host_func = self._host.download
        args = (name, url, owner, repo)
        consumer = (lambda result,
                          self=self,
                          owner=owner,
                          repo=repo: self.notify_download(owner, repo, result))
        self._threadom.run(host_func,
                             target_args=args,
                             consumer=consumer)

    def notify_auth(self, success):
        """button_style = None
        if success:
            button_style = my_theme.get_button_auth_style()
        else:
            button_style = my_theme.get_button_style()
        button_style.target(self._button_auth)"""
        pass

    def _build(self):
        self._body = tk.Frame(self._master)
        # left frame
        left_frame = self._gen_left_frame(self._body)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=1,
                        padx=(0, 10), pady=2)
        # right frame
        right_frame = self._gen_right_frame(self._body)
        right_frame.pack(side=tk.RIGHT, pady=2)

    def _on_destroy(self):
        pass

    # =====================
    #
    # =====================
    def _gen_left_frame(self, master):
        frame = tk.Frame(master)
        # search entry
        entry_search = tk.Entry(frame, width=30,
                                textvariable=self._strvar_search)
        entry_search.pack(side=tk.LEFT, padx=2)
        entry_search.bind("<Return>",
                          lambda e, self=self: self._on_click_search())
        entry_search.focus()
        # button search
        button_search = tk.Button(frame, name="button_go", text=">",
                                  command=self._on_click_search)
        button_search.pack(side=tk.LEFT)
        return frame

    def _gen_right_frame(self, master):
        # frame
        frame = tk.Frame(master, name="menu_frame")
        # button import
        button_import = tk.Button(frame,
                                  text="Import",
                                  command=self._on_click_import)
        button_import.pack(side=tk.LEFT, padx=(0, 2))
        # button export
        button_export = tk.Button(frame,
                                  text="Export",
                                  command=self._on_click_export)
        button_export.pack(side=tk.LEFT, padx=(0, 2))
        # button rate
        button_rate = tk.Button(frame,
                                text="Rate",
                                command=self._on_click_rate)
        button_rate.pack(side=tk.LEFT, padx=(0, 2))
        # button auth
        self._button_auth = tk.Button(frame,
                                      text="Auth",
                                      command=self._on_click_auth)
        self._button_auth.pack(side=tk.LEFT, padx=(0, 2))
        # button about
        button_about = tk.Button(frame,
                                 text="About",
                                 command=self._on_click_about)
        button_about.pack(side=tk.LEFT, padx=(0, 2))
        return frame

    def _on_click_search(self):
        owner, repo = self._parse_search()
        if owner is None:
            return
        self._request_an_offline_search(owner, repo)

    def _on_click_import(self):
        # check
        #if self._host.login is None:
        #    message = "Please authenticate yourself first"
        #    toast = Toast(self.body, message=message)
        #    return
        cache = os.path.expanduser("~")
        filename = filedialog.askopenfilename(initialdir=cache,
                                              title="Select a file to import")
        if not isinstance(filename, str) or not filename:
            return
        with open(filename, "r") as file:
            data = file.read()
        data = data.splitlines()
        import_list_view = ImportListView(self, self, data)
        import_list_view.build()

    def _on_click_export(self):
        target = self._host.get_list
        consumer = self.notify_list
        self._threadom.run(target, consumer=consumer)

    def _on_click_rate(self):
        target = self._host.get_rate
        consumer = lambda result, self=self: self.notify_rate(result)
        self._threadom.run(target, consumer=consumer)
        if self._toast_cache:
            return
        self._toast_cache = Toast(self._body,
                                  message="Rate Limit: Loading...",
                                  duration=None)

    def _on_click_auth(self):
        auth_view = AuthView(self)
        auth_view.build()

    def _on_click_about(self):
        about_view = AboutView(self)
        about_view.build()

    def _parse_search(self):
        search = self._strvar_search.get()
        if not search:
            return None, None
        search = search.replace("https://github.com/", "")
        self._strvar_search.set(search)
        owner, repo = self._host.parse_owner_repo(search)
        if owner is None or repo is None:
            owner = repo = None
            toast = Toast(self._body, message="Incorrect search")
        return owner, repo

    def _request_an_offline_search(self, owner, repo):
        self._toast_cache = Toast(self._body,
                                  message="Searching...",
                                  duration=None)
        host = self._host.search_offline
        args = (owner, repo)
        consumer = (lambda result,
                           self=self,
                           owner=owner,
                           repo=repo:
                    self.notify_offline_search_result(owner, repo, result))
        self._threadom.run(host,
                             target_args=args,
                             consumer=consumer,
                             sync=True)

    def _request_an_online_search(self, owner, repo):
        self._toast_cache = Toast(self._body,
                                  message="Fetching data...",
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

    def _open_app_info(self, owner, repo):
        footer_view = self._parent_view.footer_view
        app_info_view = AppInfoView(self, footer_view, owner,  repo)
        app_info_view.build()

    def _save_apps_list_in_file(self, data, path):
        cache = []
        for owner, repo in data:
            cache.append("{}/{}".format(owner, repo))
        text = "\n".join(cache)
        with open(path, "w") as file:
            file.write(text)

    def _loop_install(self, data, index=0):
        if index == len(data):
            return
        text = data[index]
        self._strvar_search.set(text)
        index += 1
        command = (lambda self=self,
                          data=data,
                          index=index:
                        self._loop_install(data, index))
        self.body.after(1000, command)
