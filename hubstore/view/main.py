import tkinter as tk
from viewable import Viewable
from threadom import Threadom
from megawidget.toast import Toast
from hubstore.host import Host
from hubstore.view.views import Views
from hubstore.view.toolbar import Toolbar
from hubstore.view.pane import Pane
from hubstore.view.about import About
from hubstore.view.installer import Installer
from hubstore.view.info import Info
from hubstore.view.report import Report
from hubstore.view.openlist import Openlist
from hubstore.view.promoted import Promoted


class Main(Viewable):

    def __init__(self, app):
        super().__init__()
        self._app = app
        self._master = app.root
        self._threadom = Threadom(app.root)
        self._views = Views()
        self._host = Host(self)
        self._views.main = self
        self._toast = None

    @property
    def app(self):
        return self._app

    @property
    def host(self):
        return self._host

    @property
    def views(self):
        return self._views

    def show_toast(self, message, duration=1234):
        self.close_toast()
        toast = Toast(self._app.root, message=message,
                      duration=duration)
        toast.update_idletasks()
        if duration is None:
            self._toast = toast

    def show_notification(self, message):
        self._views.pane.set_notification(message)

    def close_toast(self):
        if self._toast:
            self._toast.destroy()
            self._toast = None

    def clear_notification(self):
        self._views.pane.set_notification("")

    def open_toplevel_about(self):
        about = About(self)
        about.build_wait()

    def open_toplevel_installer(self, data):
        installer = Installer(self, data=data)
        installer.build_wait()

    def open_toplevel_report(self, data):
        report = Report(self, data=data)
        report.build_wait()

    def open_toplevel_info(self, data):
        info = Info(self, data=data)
        info.build_wait()

    def open_toplevel_promoted(self, data):
        promoted = Promoted(self, data=data)
        promoted.build_wait()

    def open_toplevel_openlist(self, data):
        openlist = Openlist(self, data=data)
        openlist.build_wait()

    def _build(self):
        self._body = tk.Frame(self._master)
        # install toolbar
        self._install_toolbar()
        # install pane
        self._install_pane()

    def _on_map(self):
        if self._host.on_start_app():
            # binding
            self._binding()
            self._views.toolbar.wake_search_entry()
        #from hubstore.view.downloader import Downloader
        #from hubstore.view.info import Info
        #Info(self).build()
        #Downloader(self).build()

    def _install_toolbar(self):
        toolbar = Toolbar(self._body, self._views, self._host)
        toolbar.build_pack(fill=tk.X, padx=2, pady=2)
        self._views.toolbar = toolbar

    def _install_pane(self):
        pane = Pane(self)
        pane.build_pack(expand=1, fill=tk.BOTH)
        self._views.pane = pane

    def _binding(self):
        self._body.focus_set()
        command = lambda e, views=self._views: views.toolbar.wake_search_entry()
        self._body.bind("<Control-f>", command)
        self._body.bind("<Control-F>", command)
