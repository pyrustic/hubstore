import os
import os.path
import sys
import time
import webbrowser
import subprocess
import pkgutil
from threadom import Threadom
from shared import Jason
from hubstore import core
from hubstore.misc import constant


class Host:
    def __init__(self, main_view):
        self._main_view = main_view
        self._app = main_view.app
        self._root = main_view.app.root
        self._views = main_view.views
        self._data = Data(self)
        self._initialized = None
        self._threadom = None
        self._quota = None
        self._kurl = None
        self._count_processes = 0
        self._processes = list()
        self._setup()

    @property
    def initialized(self):
        return self._initialized

    @property
    def threadom(self):
        return self._threadom

    @property
    def data(self):
        return self._data

    def on_start_app(self):
        if not self.initialized:
            self._main_view.open_toplevel_about()
        if not self.initialized:
            self._app.exit()
            return False
        apps_list = self._data.get_favorites_apps()
        title = "Favorite Apps ({})".format(len(apps_list))
        if not apps_list:
            apps_list = self._data.get_all_apps()
            title = "All Apps ({})".format(len(apps_list))
        if apps_list:
            self._views.pane.populate(title, apps_list)
            self._views.toolbar.update_apps_list(self._data.get_all_apps())
        return True

    def submit_apps_directory(self, path):
        self._initialized = False
        self._store = None
        data = core.init_hubstore(path)
        error_code = data["error_code"]
        error = data["error"]
        if error_code == 0:
            self._initialized = True
        elif error_code == 1:
            self._main_view.show_toast("Failed to create 'hubstore-apps' folder")
        elif error_code == 2:
            self._main_view.show_toast("Failed to register Hubstore in $HOME/PyrusticData")
        else:
            self._main_view.show_toast("Unknown error code")

    def open_website(self, url):
        command = lambda: webbrowser.open(url, new=2)
        self._root.after(1, command)

    def search(self, owner, repo):
        path = core.get_path(owner, repo)
        if path:
            self.show_app_info(owner, repo)
            #self._search_offline(owner, repo)
        else:
            self._search_online(owner, repo)

    def update(self, owner, repo):
        self._search_online(owner, repo)

    def rollback(self, owner, repo):
        is_success, error = core.rollback(owner, repo)
        if is_success:
            message = "Rollback done with success !"
            store = core.get_store()
            owner_repo = "{}/{}".format(owner, repo)
            data = store.get(owner_repo)
            data["backup_version"] = None
            data.save()
        else:
            message = "Failed to perform rollback"
        self._main_view.show_toast(message)

    def run_app(self, owner, repo):
        self._count_processes += 1
        process_id = self._count_processes
        self._processes.append({"id": process_id,
                                "owner": owner,
                                "repo": repo,
                                "process": None})
        target = (lambda self=self, owner=owner,
                          repo=repo, process_id=process_id:
                  self._run(owner, repo, process_id))
        consumer = (lambda error, self=self,
                           process_id=process_id:
                    self._on_app_exit(error, process_id))
        apps_open = len(self._processes)
        self._views.toolbar.update_open_count(apps_open)
        self._threadom.run(target, consumer=consumer)

    def close_app(self, process_id):
        try:
            i, data = self._get_process(process_id)
            data["process"].terminate()
        except Exception as e:
            pass

    def show_apps_from(self, owner):
        apps = self._data.get_all_apps()
        cache = []
        for x, repo in apps:
            if x == owner:
                cache.append((owner, repo))
        self._views.pane.populate("Apps from '{}' ({})".format(owner, len(cache)),
                                  cache)

    def show_app_info(self, owner, repo):
        owner_repo = "{}/{}".format(owner, repo)
        store = core.get_store()
        data = store.get(owner_repo)
        data = data.copy()
        data["owner_repo"] = owner_repo
        data["favorite"] = True if owner_repo in store.get("favorites") else False
        data["repository"] = "https://github.com/{}".format(owner_repo)
        current_time = int(time.time())
        timestamp_install = data["timestamp_install"]
        cache = current_time - timestamp_install
        cache = cache / (60*60*24)
        data["updated_since"] = int(cache)
        self._main_view.open_toplevel_info(data)

    def show_all_apps(self):
        apps_list = self._data.get_all_apps()
        title = "All Apps ({})".format(len(apps_list))
        if not apps_list:
            title = ""
        self._views.pane.populate(title, apps_list)
        self._views.toolbar.update_apps_list(self._data.get_all_apps())

    def show_favorite_apps(self):
        apps_list = self._data.get_favorites_apps()
        title = "Favorite Apps ({})".format(len(apps_list))
        if not apps_list:
            title = ""
        self._views.pane.populate(title, apps_list)

    def show_promoted(self):
        target = lambda self=self: self._show_promoted()
        consumer = (lambda data, self=self:
                    self._main_view.open_toplevel_promoted(data))
        self._threadom.run(target, consumer=consumer)

    def show_open(self):
        if not self._processes:
            self._main_view.show_toast("No app is running")
            return
        cache = []
        for item in self._processes:
            owner = item["owner"]
            repo = item["repo"]
            process_id = item["id"]
            cache.append({"owner": owner, "repo": repo,
                          "id": process_id})
        cache.reverse()
        self._main_view.open_toplevel_openlist(cache)

    def show_about(self):
        self._main_view.open_toplevel_about()

    def install(self, owner, repo, name, url):
        message = "Installation..."
        self._main_view.show_toast(message, duration=None)
        if core.get_path(owner, repo):
            is_success, error = core.backup(owner, repo)
            if not is_success:
                self._main_view.show_toast("Failed to make a backup !")
                return
        # download
        is_success, error, tempfile = core.download(name, url, self._kurl)
        if not is_success:
            self._main_view.show_toast("Failed to download the asset !")
            return
        # install
        is_success, error = core.install(owner, repo, name, tempfile)
        if not is_success:
            self._main_view.show_toast("Failed to install the asset !")
            return
        # update app information
        self._update_app_info(owner, repo)
        # update the list of apps
        message = "Successfully installed '{}/{}' !".format(owner, repo)
        self._main_view.show_toast(message)
        apps_list = self._data.get_all_apps()
        title = "All Apps ({})".format(len(apps_list))
        if apps_list:
            self._views.pane.populate(title, apps_list)
            self._views.toolbar.update_apps_list(self._data.get_all_apps())

    def uninstall(self, owner, repo):
        is_success, error = core.uninstall(owner, repo)
        message = "Successfully uninstalled !"
        if not is_success:
            message = "Failed to uninstall"
        self._main_view.show_toast(message)
        self.show_all_apps()

    def favorite(self, owner_repo, val=True):
        store = core.get_store()
        data = store.get("favorites")
        if val:
            if owner_repo not in data:
                data.append(owner_repo)
        else:
            cache = None
            for i, item in enumerate(data):
                if item == owner_repo:
                    cache = i
                    break
            if cache is not None:
                del data[cache]
        data.save()

    # ======
    def _setup(self):
        self._initialized = True
        if core.should_init_hubstore():
            self._initialized = False
        self._kurl = core.get_kurl()
        self._threadom = Threadom(self._root)

    def _search_offline(self, owner, repo):
        print("search offline 2")
        print("SEARCH OFFLINE: ", owner, repo)

    def _search_online(self, owner, repo):
        self._main_view.show_toast("Fetching...", duration=None)
        # update quota
        updated, status_text = self._update_quota()
        if not updated:
            self._main_view.show_toast("Check your connection")
            return
        # check rate
        if self._quota - 2 == 0:
            message = "You are reaching the quota limit !\nPlease try in a few minutes"
            self._main_view.show_toast(message)
            return
        # open download pane
        cache = core.fetch(owner, repo, self._kurl)
        code, error, data = cache
        self._main_view.close_toast()
        if code in (200, 304):
            self._quota -= 2
            self._main_view.open_toplevel_installer(data)
        else:
            self._main_view.show_toast(error)

    def _update_quota(self):
        if self._quota:
            return True, None
        status_code, status_text, data = core.rate(self._kurl)
        updated = False
        if status_code in (200, 304):
            self._quota = data["remaining"]
            updated = True
        return updated, status_text

    def _update_app_info(self, owner, repo):
        store = core.get_store()
        metadata = core.app_metadata(owner, repo)
        owner_repo = "{}/{}".format(owner, repo)
        info = store.get(owner_repo)
        info["version"] = metadata["version"]
        info["description"] = metadata["description"]
        info["small_img"] = metadata["small_img"]
        info["large_img"] = metadata["large_img"]
        info.save()

    def _run(self, owner, repo, process_id):
        store = core.get_store()
        app_pkg = core.get_app_pkg(owner, repo, store=store)
        path = core.get_path(owner, repo, store=store)
        try:
            p = subprocess.Popen([sys.executable, "-m", app_pkg],
                                 cwd=path, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            i, info = self._get_process(process_id)
            self._processes[i]["process"] = p
            out, err = p.communicate()
        except Exception as e:
            err = e
        return err

    def _on_app_exit(self, error, process_id):
        i, _ = self._get_process(process_id)
        if error:
            owner = self._processes[i]["owner"]
            repo = self._processes[i]["repo"]
            owner_repo = "{}/{}".format(owner, repo)
            repository = "https://github.com/{}/{}/issues".format(owner, repo)
            data = {"error": error, "owner_repo": owner_repo,
                    "repository": repository}
            self._main_view.open_toplevel_report(data)
        del self._processes[i]
        apps_open = len(self._processes)
        self._views.toolbar.update_open_count(apps_open)

    def _get_process(self, process_id):
        for i, item in enumerate(self._processes):
            if item["id"] == process_id:
                return i, item

    def _show_promoted(self):  # TODO improve + refactor this in a class
        # generate list of promoted apps
        store = core.get_store()
        apps = store.get("apps")
        cache = []
        owners_repos = []
        for owner, repos in apps.items():
            for repo in repos:
                habitat_path = core.get_path(owner, repo)
                app_pkg = core.get_app_pkg(owner, repo)
                location = os.path.join(habitat_path, app_pkg,
                                        "pyrustic_data",
                                        "hubstore")
                jason = Jason("promotion", location=location,
                              readonly=True)
                if not jason.data:
                    continue
                for owner_repo, description in jason.data.items():
                    if owner_repo in owners_repos:
                        continue
                    owners_repos.append(owner_repo)
                    cache.append({"repository": owner_repo,
                                  "description": description})
        #random.choice(cache)
        return cache


class Data:

    def __init__(self, host):
        self._host = host
        self._store = None

    @property
    def store(self):
        if not self._store:
            self._store = core.get_store()
        return self._store

    def get_apps_directory(self):
        if not self._host.initialized:
            return os.path.expanduser("~")
        location = os.path.join(constant.PYRUSTIC_DATA, "hubstore")
        jason = Jason("meta", location=location)
        return os.path.dirname(jason.data.get("hubstore-apps"))

    def get_all_apps(self):
        store = core.get_store()
        apps = store.get("apps")
        cache = []
        for owner, repos in apps.items():
            for repo in repos:
                cache.append((owner, repo))
        cache.sort(key=lambda x: x[1])
        return cache

        #return (("facebook", "whatsapp"), ("facebook", "instagram"),
        #        ("google", "search"), ("google", "android"),
        #        ("google", "chromium"))

    def get_favorites_apps(self):
        store = core.get_store()
        apps = store.get("favorites")
        cache = []
        for app in apps:
            cache.append(app.split("/"))
        return cache

    def get_image(self, owner, repo):
        store = core.get_store()
        owner_repo = "{}/{}".format(owner, repo)
        data = store.get(owner_repo)
        app_pkg = data["app_pkg"]
        small_img = data["small_img"]
        if not small_img:
            return self.get_default_image()
        habitat = core.get_path(owner, repo)
        cache = os.path.join(habitat, app_pkg)
        path = core.normpath(cache, small_img)
        if os.path.isfile(path):
            with open(path, "rb") as file:
                data = file.read()
            return data
        return self.get_default_image()

    def get_cover_image(self):
        return self.get_default_cover_image()

    def get_default_image(self):
        data = pkgutil.get_data("hubstore",
                                "asset/default_hubstore_tile_img.png")
        return data

    def get_default_cover_image(self):
        data = pkgutil.get_data("hubstore",
                                "asset/default_cover.png")
        return data
