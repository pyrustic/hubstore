import sys
import subprocess
import os.path
import operator
from hubstore import about as hubstore_about
from hubstore.host import core
from pyrustic.jasonix import Jasonix
from pyrustic.gurl import Gurl


class MainHost:

    def __init__(self):
        self._count_processes = 0
        self._processes = dict()
        self._login = None
        self._gurl = core.get_gurl()
        self._download_gurl = self._get_download_gurl()

    # === PROPERTIES ===
    @property
    def login(self):
        return self._login

    # === PUBLIC ===

    def should_init_hubstore(self):
        """
        Return a boolean to tell if the method
        "init_hubstore()" should be called or not
        """
        return core.should_init_hubstore()

    def init_hubstore(self, path):
        """
        Initialize Hubstore.

        Param:
            - path: absolute path in which the folder "hubstore-apps"
            will be created

        Return:
            A dict: {"error_code": int, "error": object, "root_dir": str}
            - The "error_code" is one of:
                0 = all right
                1 = failed to create "hubstore-apps" folder
                2 = failed to register Hubstore in $HOME/PyrusticData
            - "root_dir" is the absolute path to the folder "hubstore-apps".
        """
        return core.init_hubstore(path)

    def auth(self, token):
        """
        Return: (status_code, status_text, login_str)
        data = the login if status is 200 or 304, else data is None
        """
        status_code, status_text, self._login = core.auth(token, self._gurl)
        return status_code, status_text, self._login

    def unauth(self):
        self._gurl.token = None
        self._login = None

    def parse_owner_repo(self, val):
        """
        Param:
            val: string
        Return:
            A tuple of strings as ("owner", "repo")
            or a tuple of None as (None, None)
        """
        return core.parse_owner_repo(val)

    def search_offline(self, owner, repo):
        """
        Param
            owner and repo are strings
        Return
            Boolean.
        """
        path = core.path(owner, repo)
        if not path:
            return False
        return os.path.exists(path)

    def search_online(self, owner, repo):
        """
        Return:
        {"success": bool,
                "status": tuple(status_code, status_text),
                "release": dict of useful data,
                "assets": list of dicts}"""
        success = None
        status = None
        release = None
        assets = None
        status_code, status_text, data = core.fetch(owner,
                                                    repo,
                                                    self._gurl)
        status = (status_code, status_text)
        if status_code in (200, 304):
            success = True
            useful_info = core.useful_info(data)
            assets = useful_info["assets"]
            del useful_info["assets"]
            release = useful_info
        else:
            success = False
        data = {"success": success,
                "status": status,
                "release": release,
                "assets": assets}
        return data

    def download(self, name, url, owner, repo):
        """ Return {"success": bool, "error": object}"""
        # download
        is_success, error, tempfile, name = core.download(name,
                                                          url,
                                                          self._download_gurl)
        data = {"success": is_success, "error": error}
        if not is_success:
            return data
        # backup
        is_success, error = core.backup(owner, repo)
        if not is_success and error is not None:
            data["success"] = is_success
            data["error"] = error
            return data
        # unpack
        is_success, error = core.unpack(name, tempfile, owner, repo)
        if not is_success:
            data["success"] = is_success
            data["error"] = error
            return data
        # TODO: implement pip install -? requirement.txt
        # TODO: implement find install script
        # TODO: implement Run install script
        data["success"] = True
        data["None"] = None
        return data

    def run(self, owner, repo, callback_process_id):
        self._count_processes += 1
        process_id = self._count_processes
        callback_process_id(owner, repo, process_id)
        data = {"is_success": True, "error": None,
                "id": process_id,
                "owner": owner, "repo": repo}
        path = core.path(owner, repo)
        try:
            p = subprocess.Popen([sys.executable, "main.py"],
                                 cwd=path,
                                 stderr=subprocess.PIPE)
            self._processes[process_id] = p
            out, err = p.communicate()
            data["error"] = err
        except Exception as e:
            data["is_success"] = False
            data["error"] = e
        return data
    
    def get_rate(self):
        """
        Get Rate Limit
        Return:
             {"status_code": int, "status_text": str,
              "data": data}
        data = {"limit": int, "remaining": int}
        """
        status_code, status_text, data = core.rate(self._gurl)
        return {"status_code": status_code,
                "status_text": status_text,
                "data": data}

    def get_list(self):
        """
        Return success_bool, error, data
        Data is the list of apps like this:
            [ ("owner_1", "repo_1"), ("owner_2", "repo_2"),
              ("owner_3", "repo_3"), ("owner_4", "repo_4") ]
        """
        is_success, error, data = core.get_list()
        if not is_success:
            return False, error, None
        cache = []
        for key, val in data.items():
            for item in val:
                cache.append((key, item))
        return True, None, sorted(cache, key=operator.itemgetter(1))

    def rollback(self, owner, repo):
        """ Rollback. Return boolean is_success, error """
        return core.rollback(owner, repo)

    def uninstall(self, owner, repo):
        """
        Delete an app by giving its owner and repo.
        Return bool is_success, error
        """
        return core.uninstall(owner, repo)

    def get_info(self, owner, repo):
        """ Return None or data.
        data:
            {"owner": str, "repo": str,
             "path": str, "email": str,
             "version": str,
             "description": str,
             "homepage": str}
        """
        root_dir = core.path(owner, repo)
        data = {"owner": owner, "repo": repo,
                "path": root_dir, "email": None,
                "version": None,
                "description": None,
                "homepage": None}
        app_json_path = os.path.join(root_dir, "pyrustic_data", "app.json")
        if not os.path.exists(app_json_path):
            return data
        jasonix = Jasonix(app_json_path)
        data["version"] = jasonix.data.get("version", "None")
        data["email"] = jasonix.data.get("email", None)
        data["description"] = jasonix.data.get("description", None)
        data["homepage"] = jasonix.data.get("home_page", None)
        return data

    def get_image(self, owner, repo):
        """ Return None or path"""
        root_dir = core.path(owner, repo)
        hubstore_json_path = os.path.join(root_dir, "pyrustic_data", "hubstore.json")
        path = None
        if os.path.exists(hubstore_json_path):
            jasonix = Jasonix(hubstore_json_path)
            path = jasonix.data.get("showcase_small_img", None)
            if path:
                path = path.replace("./", "", 1) if path.startswith("./") else path
                path = os.path.join(root_dir, path)
        if not path or not os.path.exists(path):
            path = self._get_default_image()
        return path

    def stop_process(self, process_id):
        if process_id not in self._processes:
            return
        try:
            self._processes[process_id].terminate()
        except Exception as e:
            pass
        del self._processes[process_id]


    # === PRIVATE ===
    def _get_default_image(self):
        root_dir = hubstore_about.ROOT_DIR
        path = os.path.join(root_dir, "misc", "default.png")
        if not os.path.exists(path):
            path = None
        return path

    def _get_download_gurl(self):
        """
        Generate a Gurl object
        """
        headers = {"Accept": "application/octet-stream",
                   "User-Agent": "Pyrustic"}
        gurl = Gurl(headers=headers)
        return gurl
