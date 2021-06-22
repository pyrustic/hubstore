import sys
import subprocess
import os.path
import operator
import pkgutil
from hubstore.host import core
from pyrustic.manager import constant
from jayson import Jayson
from kurl import Kurl


class MainHost:

    def __init__(self):
        self._count_processes = 0
        self._processes = dict()
        self._login = None
        self._kurl = core.get_kurl()
        self._download_kurl = self._get_download_kurl()
        self._setup()

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
        status_code, status_text, self._login = core.auth(token, self._kurl)
        return status_code, status_text, self._login

    def unauth(self):
        self._kurl.token = None
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
                                                    self._kurl)
        status = (status_code, status_text)
        if status_code in (200, 304):
            success = True
            useful_info = core.useful_info(data)
            assets = useful_info["assets"]
            del useful_info["assets"]
            release = useful_info
        else:
            success = False
        assets = self._filter_assets(assets)
        data = {"success": success,
                "status": status,
                "release": release,
                "assets": assets}
        return data

    def download(self, name, url, owner, repo):
        """ Return {"success": bool, "error": object}"""
        # download
        is_success, error, name = core.download(owner,
                                                repo,
                                                name,
                                                url,
                                                self._download_kurl)
        data = {"success": is_success, "error": error}
        if not is_success:
            return data
        # backup
        is_success, error = core.backup(owner, repo)
        if not is_success and error is not None:
            data["success"] = is_success
            data["error"] = error
            return data
        # install
        is_success, error = core.install(owner, repo, name)
        if not is_success:
            data["success"] = is_success
            data["error"] = error
            return data
        # TODO: implement pip install -? requirement.txt
        # TODO: implement find install script
        # TODO: implement Run install script
        # TODO: also uninstall script !
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
        app_pkg = core.get_app_pkg(owner, repo)
        try:
            p = subprocess.Popen([sys.executable, "-m", app_pkg],
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
        status_code, status_text, data = core.rate(self._kurl)
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
                cache.append((key, item[0]))
        return True, None, sorted(cache, key=operator.itemgetter(1))

    def rollback(self, owner, repo):
        """ Rollback. Return boolean is_success, error """
        is_success, error = core.rollback(owner, repo)
        return is_success, error

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
        if root_dir is None:
            return data
        path = None
        for item in os.listdir(root_dir):
            if item.startswith(repo) and item.endswith("dist-info"):
                path = os.path.join(root_dir, item, "METADATA")
                break
        if path is None:
            return data
        if not os.path.exists(path):
            return data
        metadata = self._metadata(path)
        data["version"] = metadata["version"]
        data["email"] = metadata["email"]
        data["description"] = metadata["description"]
        data["homepage"] = metadata["homepage"]
        return data

    def get_image(self, owner, repo):
        """ Return None or path"""
        root_dir = core.path(owner, repo)
        app_pkg = core.get_app_pkg(owner, repo)
        hubstore_json_path = os.path.join(root_dir, app_pkg,
                                          "pyrustic_data", "hubstore.json")
        data = None
        if os.path.exists(hubstore_json_path):
            jayson = Jayson(hubstore_json_path)
            path = jayson.data.get("showcase_small_img", None)
            if path:
                path = path.replace("./", "", 1) if path.startswith("./") else path
                path = os.path.join(root_dir, repo, path)
                with open(path, "rb") as file:
                    data = file.read()
        if not data:
            data = self._get_default_image()
        return data

    def stop_process(self, process_id):
        if process_id not in self._processes:
            return
        try:
            self._processes[process_id].terminate()
        except Exception as e:
            pass
        del self._processes[process_id]

    def _setup(self):
        shared_folder = os.path.join(constant.SHARED_PYRUSTIC_DATA,
                                     "hubstore")
        shared_json_path = os.path.join(shared_folder,
                                        "hubstore_shared_data.json")
        if not os.path.exists(shared_folder):
            os.makedirs(shared_folder)
        if not os.path.exists(shared_json_path):
            resource = "misc/default_json/default_shared_data.json"
            default_json = pkgutil.get_data("hubstore",
                                            resource)
            with open(shared_json_path, "wb") as file:
                file.write(default_json)
        self._jayson = Jayson(shared_json_path)

    # === PRIVATE ===
    def _filter_assets(self, assets):
        assets = [] if not assets else assets
        cache = []
        for asset in assets:
            _, ext = os.path.splitext(asset["name"])
            if ext == ".whl":
                cache.append(asset)
        return cache

    def _get_default_image(self):
        resource = "misc/default.png"
        data = pkgutil.get_data("hubstore", resource)
        return data

    def _get_download_kurl(self):
        """
        Generate a Kurl object
        """
        headers = {"Accept": "application/octet-stream",
                   "User-Agent": "Pyrustic"}
        kurl = Kurl(headers=headers)
        return kurl

    def _metadata(self, path):
        data = {"email": None, "version": None, "description": None,
                "homepage": None}
        raw = self._dirty_metadata_parser(path)
        mapping = {"Version": "version",
                   "Author-email": "email",
                   "Maintainer-email": "email",
                   "Summary": "description",
                   "Home-page": "homepage"}
        for item in raw:
            key, value = item
            if key in mapping:
                data[mapping[key]] = value
        return data


    def _dirty_metadata_parser(self, path):
        data = []
        with open(path, "r") as file:
            for line in file.readlines():
                key = ""
                value = ""
                parsing_key = True
                parsing_value = False
                cache = ""
                if line == "\n":
                    break
                for char in line:
                    if parsing_key and char == ":":
                        parsing_key = False
                        key = cache
                        cache = ""
                        continue
                    if not parsing_key and not parsing_value:
                        parsing_value = True
                        continue
                    if parsing_value and char == "\n":
                        value = cache
                        data.append((key, value))
                    cache += char
        return data


