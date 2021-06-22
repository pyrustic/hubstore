import webbrowser
import tkinter as tk
from viewable import Viewable
from megawidget.toast import Toast
from megawidget.confirm import Confirm
from hubstore.view.downloader_view import DownloaderView


class AppInfoView(Viewable):
    def __init__(self, parent_view, footer_view, owner, repo):
        super().__init__()
        self._parent_view = parent_view
        self._footer_view = footer_view
        self._owner = owner
        self._repo = repo
        self._master = parent_view.body
        self._host = parent_view.host
        self._threadom = parent_view.threadom
        self._body = None
        self._text_description = None
        self._toast_cache = None
        # stringvars
        self._strvar_path = tk.StringVar()
        self._strvar_owner = tk.StringVar()
        self._strvar_repo = tk.StringVar()
        self._strvar_email = tk.StringVar()
        self._strvar_version = tk.StringVar()
        self._strvar_homepage = tk.StringVar()

    def notify_update(self, owner, repo, result):
        if self._toast_cache:
            self._toast_cache.destroy()
            self._toast_cache = None
        success = result["success"]
        status = result["status"]
        if not success:
            message = "Failed to fetch data\n{} {}".format(status[0], status[1])
            Toast(self._body, message=message)
        else:
            self.destroy()
            header_view = self._parent_view.header_view
            downloader_view = DownloaderView(header_view,
                                             owner, repo,
                                             result["release"],
                                             result["assets"])
            downloader_view.build()

    def notify_rollback(self, result):
        is_success, error = result
        message = "Successfully made a rollback !"
        if not is_success:
            message = "Failed to rollback"
        toast = Toast(self._body, message=message)
        toast.wait_window()
        if is_success:
            self._parent_view.load_data()
            self.destroy()

    def notify_uninstall(self, result):
        is_success, error = result
        if is_success:
            message = "Successfully uninstalled"
        else:
            message = "Failed to uninstall the app"
        Toast(self._body, message=message).wait_window()
        if is_success:
            self._parent_view.load_data()
            self.destroy()

    def _build(self):
        self._body = tk.Toplevel(self._master, name="toplevel_app_info")
        self._body.title("App Info")
        # gen header frame
        frame_header = self._gen_header_frame(self._body)
        frame_header.pack(fill=tk.X)
        # gen central frame
        frame_central = self._gen_central_frame(self._body)
        frame_central.pack(fill=tk.BOTH,
                           expand=1, padx=5, pady=(20, 30))
        # gen footer
        frame_footer = self._gen_footer_frame(self._body)
        frame_footer.pack(fill=tk.X, pady=2)

    def _on_map(self):
        super()._on_map()
        self._populate()

    def _on_destroy(self):
        pass

    def _gen_header_frame(self, master):
        frame = tk.Frame(master)
        # Label Path
        label_path = tk.Label(frame, name="label_path", text="Path:")
        label_path.pack(side=tk.LEFT)
        # Entry path
        entry_path = tk.Entry(frame, name="entry_path", state="readonly",
                              textvariable=self._strvar_path)
        entry_path.pack(expand=1, fill=tk.X, side=tk.LEFT, pady=2)
        # Button copy
        button_copy = tk.Button(frame, text="Copy",
                                command=self._on_click_copy)
        button_copy.pack(side=tk.LEFT, pady=2, padx=(2, 2))
        return frame

    def _gen_central_frame(self, master):
        frame = tk.Frame(master, name="central_frame")
        # == owner frame
        frame_owner = tk.Frame(frame)
        frame_owner.grid(row=0, column=0, sticky="w",
                         padx=(0, 5), pady=(0, 7))
        # owner label
        label_owner = tk.Label(frame_owner, text="Owner")
        label_owner.pack(anchor="w")
        # owner entry
        entry_owner = tk.Entry(frame_owner,
                               width=20,
                               state="readonly",
                               textvariable=self._strvar_owner)
        entry_owner.pack(anchor="w")
        # == repo frame
        frame_repo = tk.Frame(frame)
        frame_repo.grid(row=0, column=1,
                        sticky="w",
                        padx=(0, 5), pady=(0, 7))
        # repo label
        label_repo = tk.Label(frame_repo, text="Repository")
        label_repo.pack(anchor="w")
        # repo entry
        entry_repo = tk.Entry(frame_repo,
                              width=20,
                              state="readonly",
                              textvariable=self._strvar_repo)
        entry_repo.pack(anchor="w")
        # == email frame
        frame_email = tk.Frame(frame)
        frame_email.grid(row=0, column=2,
                         sticky="w",
                         pady=(0, 7))
        # email label
        label_email = tk.Label(frame_email, text="Email")
        label_email.pack(anchor="w")
        # email entry
        entry_email = tk.Entry(frame_email,
                               width=20,
                               state="readonly",
                               textvariable=self._strvar_email)
        entry_email.pack(anchor="w")
        # == version frame
        frame_version = tk.Frame(frame)
        frame_version.grid(row=1, column=0,
                           sticky="w",
                           pady=(0, 7))
        # version label
        label_version = tk.Label(frame_version, text="Version")
        label_version.pack(anchor="w")
        # version entry
        entry_version = tk.Entry(frame_version,
                                 width=20,
                                 state="readonly",
                                 textvariable=self._strvar_version)
        entry_version.pack(anchor="w")
        # == home page
        frame_homepage = tk.Frame(frame)
        frame_homepage.grid(row=1, column=1, columnspan=2,
                            sticky="we",
                            pady=(0, 7))

        # homepage label
        label_homepage = tk.Label(frame_homepage, text="Homepage")
        label_homepage.pack(anchor="w")
        # sub frame homepage
        sub_frame_homepage = tk.Frame(frame_homepage)
        sub_frame_homepage.pack(fill=tk.X)
        # homepage entry
        entry_homepage = tk.Entry(sub_frame_homepage,
                                  state="readonly",
                                  width=20,
                                  textvariable=self._strvar_homepage)
        entry_homepage.pack(side=tk.LEFT, expand=1,
                            fill=tk.X, anchor="w",
                            padx=(0, 2))
        # button visit
        button_visit = tk.Button(sub_frame_homepage, text="Visit",
                                 command=self._on_click_homepage)
        button_visit.pack(side=tk.LEFT, ipady=0, ipadx=0)
        # == description frame
        frame_description = tk.Frame(frame)
        frame_description.grid(row=2, column=0,
                               columnspan=3,
                               sticky="we",
                               pady=(0, 7))
        # description label
        label_description = tk.Label(frame_description,
                                     text="Description")
        label_description.pack(anchor="w")
        # description text
        self._text_description = tk.Text(frame_description,
                                         width=1, height=7,
                                         state="disabled")
        self._text_description.pack(anchor="w", fill=tk.X)

        return frame

    def _gen_footer_frame(self, master):
        frame = tk.Frame(master)
        # Button RUN
        button_run = tk.Button(frame, text="Run",
                               command=self._on_click_run)
        button_run.pack(side=tk.RIGHT, padx=1)
        # Button UPDATE
        button_update = tk.Button(frame, text="Update",
                                  command=self._on_click_update)
        button_update.pack(side=tk.RIGHT, padx=1)
        # Button ROLLBACK
        button_rollback = tk.Button(frame, text="Rollback",
                                    command=self._on_click_rollback)
        button_rollback.pack(side=tk.RIGHT, padx=1)
        # Button UNINSTALL
        button_uninstall = tk.Button(frame, text="Uninstall",
                                     command=self._on_click_uninstall)
        button_uninstall.pack(side=tk.RIGHT, padx=1)
        # Button CANCEL
        button_cancel = tk.Button(frame, text="Cancel",
                                  command=self.destroy)
        button_cancel.pack(side=tk.RIGHT, padx=1)
        return frame

    def _populate(self):
        data = self._host.get_info(self._owner, self._repo)
        if data is None:
            toast = Toast(self._body, message="Failed to load app information")
            self.destroy()
            return
        #
        self._strvar_path.set(data["path"]) if data["path"] else None
        self._strvar_owner.set(data["owner"]) if data["owner"] else None
        self._strvar_repo.set(data["repo"]) if data["repo"] else None
        self._strvar_email.set(data["email"]) if data["email"] else None
        self._strvar_version.set(data["version"]) if data["version"] else None
        self._strvar_homepage.set(data["homepage"]) if data["homepage"] else None
        # text description
        self._text_description.config(state="normal")
        self._text_description.insert("1.0", data["description"]
                                      if data["description"]
                                      else "")
        self._text_description.config(state="disabled")

    def _on_click_copy(self):
        self._body.clipboard_clear()
        self._body.clipboard_append(self._strvar_path.get())

    def _on_click_run(self):
        target = self._host.run
        args = (self._owner, self._repo,
                self._footer_view.add_item)
        consumer = self._footer_view.exited_app
        self._threadom.run(target, target_args=args, consumer=consumer)

    def _on_click_update(self):
        self._toast_cache = Toast(self._body,
                                  message="Fetching...",
                                  duration=None)
        owner = self._owner
        repo = self._repo
        host = self._host.search_online
        args = (self._owner, self._repo)
        consumer = (lambda result,
                           self=self,
                           owner=owner,
                           repo=repo:
                    self.notify_update(owner, repo, result))
        self._threadom.run(host,
                           consumer=consumer,
                           target_args=args,
                           sync=True)

    def _on_click_uninstall(self):
        header = "Confirm"
        message = "You are going to uninstall an app."
        message += "\nDo you really want to continue ?"
        confirm = Confirm(self._body,
                          header=header,
                          message=message)
        confirm.wait_window()
        if not confirm.ok:
            return
        target = self._host.uninstall
        args = (self._owner, self._repo)
        consumer = self.notify_uninstall
        self._threadom.run(target, target_args=args, consumer=consumer)

    def _on_click_rollback(self):
        header = "Confirm"
        message = "You are going to rollback an app."
        message += "\nDo you really want to continue ?"
        confirm = Confirm(self._body,
                          header=header,
                          message=message)
        confirm.wait_window()
        if not confirm.ok:
            return
        target = self._host.rollback
        args = (self._owner, self._repo)
        consumer = self.notify_rollback
        self._threadom.run(target, target_args=args, consumer=consumer)

    def _on_click_homepage(self):
        homepage = self._strvar_homepage.get()
        if not homepage:
            homepage = "https://github.com/{}/{}".format(self._owner,
                                                         self._repo)
        target = webbrowser.open
        kwargs = {"url": homepage, "new": 2}
        self._threadom.run(target, target_kwargs=kwargs)
