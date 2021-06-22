import tkinter as tk
from viewable import Viewable
from megawidget.toast import Toast


class AuthView(Viewable):

    def __init__(self, parent_view):
        super().__init__()
        self._parent_view = parent_view
        self._master = self._parent_view.body
        self._host = self._parent_view.host
        self._threadom = self._parent_view.threadom
        self._body = None
        self._strvar = tk.StringVar()
        self._is_auth = self._check_is_auth()
        self._toast_cache = None

    def notify_auth(self, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        status_code, status_text, login = result
        if status_code not in (200, 304):
            message = "Failed to authenticate\n{} {}".format(status_code,
                                                             status_text)
            Toast(self._body, message=message)
            self._parent_view.notify_auth(False)
            return
        self.destroy()
        message = "Welcome {} !".format(login)
        toast = Toast(self._parent_view.body, message=message)
        toast.wait_window()
        self._parent_view.notify_auth(True)

    def _build(self):
        self._body = tk.Toplevel(self._master, name="auth_view")
        self._body.resizable(False, False)
        # title
        label_title = tk.Label(self._body, text="Token")
        label_title.pack(anchor="w", padx=2, pady=(5, 0))
        # entry
        entry_token = tk.Entry(self._body, show="*", width=20,
                               textvariable=self._strvar)
        entry_token.pack(anchor="w", padx=2)
        entry_token.focus_set()
        # footer
        frame_footer = tk.Frame(self._body)
        frame_footer.pack(fill=tk.BOTH, pady=(20, 0))
        # button connect
        button_connect = tk.Button(frame_footer, text="Connect",
                                   command=self._on_click_connect)
        button_connect.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        # button cancel
        button_cancel = tk.Button(frame_footer, text="Cancel",
                                  command=self._on_click_cancel)
        button_cancel.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        # alter gui if not auth
        if self._is_auth:
            self._alter_gui_auth_mode(label_title, entry_token,
                                      button_connect)

    def _on_destroy(self):
        pass

    # =======================
    #
    # =======================
    def _check_is_auth(self):
        if self._host.login is None:
            return False
        return True

    def _alter_gui_auth_mode(self, label_title, entry_token, button_connect):
        # label title
        label_title.config(text="Login")
        # entry token
        entry_token.insert(0, self._host.login)
        entry_token.config(state="readonly", show="")
        # button connect
        button_connect.config(text="Disconnect",
                              command=self._on_click_disconnect)

    def _on_click_connect(self):
        token = self._strvar.get()
        if token == "":
            return
        target = self._host.auth
        args = (token, )
        consumer = self.notify_auth
        self._threadom.run(target, target_args=args,
                           consumer=consumer)
        self._toast_cache = Toast(self._body,
                                  message="Authenticating...",
                                  duration=None)

    def _on_click_disconnect(self):
        self._host.unauth()
        Toast(self._body, message="Disconnected").wait_window()
        self._parent_view.notify_auth(False)
        self.destroy()

    def _on_click_cancel(self):
        self.destroy()
