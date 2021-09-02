import os
import os.path
import uuid
import shutil
import subprocess
import sys
import time
import random
from hubstore.misc import funcs
from tempfile import TemporaryDirectory
from hubstore.misc import constant
from kurl import Kurl
from shared import Store, Jason, valid_store, valid_jason


def get_store():
    """
    Returns the main store datastore if it exists,
    else returns None
    """
    cache = os.path.join(constant.PYRUSTIC_DATA, "hubstore")
    if not valid_jason(os.path.join(cache, "meta.json")):
        return None
    jason = Jason("meta", location=cache)
    if not jason.data:
        return None
    path = jason.data.get("hubstore-apps")
    if not path:
        return None
    cache = os.path.join(path, "data")
    if not valid_store(cache):
        return None
    return Store("data", location=path)


def should_init_hubstore():
    if get_store():
        return False
    return True


def init_hubstore(path):
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
        - "root_dir" is the absolute path to the folder "hubstore-apps".
        Example: init_hubstore("/path/to/use") will return this "root_dir":
            "/path/to/use/hubstore-apps"
        Inside "hubstore-apps", two main folders:
            - apps: to store apps by owner. Meaning that visible folders
            in "apps" are owners, and inside each owner there are a repo
            - data: this is where the library Store stores data.
    """
    error_code = 0
    error = None
    root_dir = None
    data = {"error_code": error_code,
            "error": error,
            "root_dir": root_dir}
    # create hubstore-apps
    error, root_dir = _create_hubstore_apps_folder(path)
    if error is not None:
        data["error_code"] = 1
        data["error"] = error
        return data
    # register Hubstore in PyrusticData
    _register_hubstore_in_pyrustic_data(root_dir)
    data["root_dir"] = root_dir
    return data


def rate(kurl):
    """
    Get Rate Limit
    Return: status_code, status_text, data
    data = {"limit": int, "remaining": int}
    """
    target = "https://api.github.com"
    url = "{}/rate_limit".format(target)
    response = kurl.request(url)
    json = response.json
    status_code, status_text = response.status
    data = {}
    if status_code == 304:
        data = response.cached_response.json
    if (status_code in (200, 304)) and json:
        data["limit"] = json["resources"]["core"]["limit"]
        data["remaining"] = json["resources"]["core"]["remaining"]
    return status_code, status_text, data


def fetch(owner, repo, kurl):
    """ Fetch resource
    Param:
        - owner: str
        - repo: str
        - kurl: Kurl object

    Return:
        status_code, status_text, json_data
        Json_data: {"description": str, "stargazers": int,
                    "tag": str, "published_at": str,
                    "downloads": int, "size": int,
                    "repository": str, "owner_repo": str,
                    "assets": list}
    """
    # fetch repo description
    data = dict()
    data["owner_repo"] = "{}/{}".format(owner, repo)
    data["repository"] = "https://github.com/{}/{}".format(owner, repo)
    status_code, status_text, json = fetch_description(owner, repo, kurl)
    if status_code in (200, 304):
        data["description"] = json["description"]
        data["stargazers"] = json["stargazers_count"]
        status_code, status_text, json = fetch_latest_release(owner, repo, kurl)
        if status_code in (200, 304):
            data["tag"] = json["tag_name"]
            data["published_at"] = funcs.badass_iso_8601_date_parser(json["published_at"])
            data["assets"] = []
            for asset in json["assets"]:
                _, ext = os.path.splitext(asset["name"])
                if ext != ".whl":
                    continue
                cache = {"name": asset["name"],
                         "size": asset["size"],
                         "url": asset["browser_download_url"],
                         "download_count": asset["download_count"],
                         "content_type": asset["content_type"]}
                data["assets"].append(cache)
    return status_code, status_text, data


def useful_info(data):
    """ Return useful info in a dict. Return None if the dict data is empty """
    if not data:
        return None
    info = {"tag_name": data["tag_name"],
            "published_at": funcs.badass_iso_8601_date_parser(data["published_at"]),
            "assets": []}
    for asset in data["assets"]:
        cache = {"name": asset["name"],
                 "size": asset["size"],
                 "url": asset["browser_download_url"],
                 "created_at": funcs.badass_iso_8601_date_parser(asset["created_at"]),
                 "updated_at": funcs.badass_iso_8601_date_parser(asset["updated_at"]),
                 "uploader_login": asset["uploader"]["login"],
                 "download_count": asset["download_count"],
                 "content_type": asset["content_type"]}
        info["assets"].append(cache)
    return info


def download(name, url, kurl):
    """
    Download the resource (url) with kurl object
    Return a boolean is_success, error, and tempdata
    Tempdata: (tempdir, filename)
    """
    is_success = True
    error = None
    response = kurl.request(url)
    data = response.body
    if response.code == 304:
        if response.cached_response:
            data = response.cached_response.body
    if data is None:
        return None, "The server returned an empty body", None
    tempdir = None
    filename = None
    try:
        tempdir = TemporaryDirectory()
        filename = os.path.join(tempdir.name, name)
        with open(filename, "wb") as file:
            file.write(data)
    except Exception as e:
        error = e
        is_success = False
    tempdata = {"tempdir": tempdir, "filename": filename}
    return is_success, error, tempdata


def install(owner, repo, name, tempdata):
    """
    Install the cached wheel file
    Return bool is_success, error
    """
    is_success, error = _install(owner, repo, tempdata)
    if not is_success:
        return False, error
    store = get_store()
    app_pkg = name.split("-")[0]
    apps = store.get("apps")
    if owner not in apps:
        apps[owner] = list()
    if repo not in apps[owner]:
        apps[owner].append(repo)
    apps.save()
    owner_repo = "{}/{}".format(owner, repo)
    timestamp_install = int(time.time())
    if not store.get(owner_repo):
        cache = {"app_pkg": app_pkg, "description": None,
                 "version": None, "small_img": None,
                 "large_img": None, "timestamp_install": timestamp_install,
                 "backup_version": None}
        store.set(owner_repo, cache)
    else:
        data = store.get(owner_repo)
        data["app_pkg"] = app_pkg
        data["timestamp_install"] = timestamp_install
        data.save()
    return True, None


def app_metadata(owner, repo):
    store = get_store()
    owner_repo = "{}/{}".format(owner, repo)
    probed_data = store.get(owner_repo)
    app_pkg = probed_data["app_pkg"]
    #app_pkg = store.get("{}/{}".format(owner, repo))["app_pkg"]
    path = get_path(owner, repo, store=store)
    data = {"version": None, "description": None,
            "small_img": None, "large_img": None}
    metadata_filename = None
    for item in os.listdir(path):
        if item.startswith(app_pkg) and item.endswith("dist-info"):
            metadata_filename = os.path.join(path, item, "METADATA")
            break
    if metadata_filename is None:
        return data
    raw = funcs.dirty_metadata_parser(metadata_filename)
    mapping = {"Version": "version",
               "Summary": "description"}
    for item in raw:
        key, value = item
        if key in mapping:
            data[mapping[key]] = value

    # extract data from $APP_PKG/pyrustic_data/hubstore
    pyrustic_data = os.path.join(path, app_pkg,
                                 "pyrustic_data",
                                 "hubstore")
    jason = Jason("img", location=pyrustic_data)
    if jason.data:
        data["small_img"] = jason.data.get("small_img")
        data["large_img"] = jason.data.get("large_img")
    return data


def backup(owner, repo):
    """
    Backup the current version of owner/repo
    Return bool is_success, error
    """
    # variables
    is_success = True
    error = None
    hubstore_apps = get_store().location
    owner_folder = os.path.join(hubstore_apps, "apps", owner)
    repo_folder = os.path.join(owner_folder, repo)
    habitat_folder = os.path.join(repo_folder, "habitat")
    backup_folder = os.path.join(repo_folder, "backup")
    backup_habitat_folder = os.path.join(backup_folder, "habitat")
    # if the repo habitat doesn't exist, return
    if not os.path.exists(habitat_folder):
        return False, None
    # create backup folder if it doesn't exist
    if not os.path.exists(backup_folder):
        try:
            os.makedirs(backup_folder)
        except Exception as e:
            return False, e
    # move habitat backup into trash if it exists
    if os.path.exists(backup_habitat_folder):
        trash = os.path.join(constant.PYRUSTIC_DATA, "trash")
        if not os.path.exists(trash):
            try:
                os.makedirs(trash)
            except Exception as e:
                return False, e
        while True:
            random_data = str(uuid.uuid4().hex)
            cache = os.path.join(trash, random_data)
            if not os.path.exists(cache):
                break
        moveto_is_success, moveto_error = _moveto(backup_habitat_folder, cache)
        if not moveto_is_success:
            return False, moveto_error
    # get app metadata
    # TODO
    # move habitat into backup folder
    src = habitat_folder
    dest = backup_folder
    is_success, error = _moveto(src, dest)
    if is_success:
        # save metadata
        owner_repo = "{}/{}".format(owner, repo)
        store = get_store()
        data = store.get(owner_repo)
        data["backup_version"] = data["version"]
        data.save()
        return True, None
    return is_success, error


def rollback(owner, repo):
    """
    Rollback. Return boolean is_success, error
    """
    # variables
    is_success = True
    error = None
    hubstore_apps = get_store().location
    owner_folder = os.path.join(hubstore_apps, "apps", owner)
    repo_folder = os.path.join(owner_folder, repo)
    habitat_folder = os.path.join(repo_folder, "habitat")
    backup_folder = os.path.join(repo_folder, "backup")
    backup_habitat_folder = os.path.join(backup_folder, "habitat")
    # if the backup habitat doesn't exist, return
    if not os.path.exists(backup_habitat_folder):
        return False, None
    # create backup folder if it doesn't exist
    #if not os.path.exists(backup_folder):
    #    try:
    #        os.makedirs(backup_folder)
    #    except Exception as e:
    #        return False, e
    # move habitat folder into trash if it exists
    if os.path.exists(habitat_folder):
        cache = os.path.join(constant.PYRUSTIC_DATA, "trash")
        if not os.path.exists(cache):
            try:
                os.makedirs(cache)
            except Exception as e:
                return False, e
        while True:
            random_data = str(uuid.uuid4().hex)
            cache = os.path.join(cache, random_data)
            if not os.path.exists(cache):
                break
        cache = _moveto(habitat_folder, cache)
        if not cache[0]:
            return False, cache[1]
    # move backup habitat folder into repo folder
    src = backup_habitat_folder
    dest = repo_folder
    if os.path.exists(src):
        is_success, error = _moveto(src, dest)
    return is_success, error


def uninstall(owner, repo):
    """
    Uninstall an app by providing its owner and repo.
    Return bool is_success, error
    """
    is_success = None
    error = None
    hubstore_apps = get_store().location
    owner_folder = os.path.join(hubstore_apps, "apps", owner)
    repo_folder = os.path.join(owner_folder, repo)
    habitat_folder = os.path.join(repo_folder, "habitat")
    backup_folder = os.path.join(repo_folder, "backup")
    backup_habitat_folder = os.path.join(backup_folder, "habitat")
    # if the repo folder doesn't exist, return
    if not os.path.exists(repo_folder):
        return False, None
    cache = os.path.join(constant.PYRUSTIC_DATA, "trash")
    if not os.path.exists(cache):
        try:
            os.makedirs(cache)
        except Exception as e:
            return False, e
    while True:
        random_data = str(uuid.uuid4().hex)
        cache = os.path.join(cache, random_data)
        if not os.path.exists(cache):
            break
    is_success, error = _moveto(repo_folder, cache)
    if is_success:
        store = get_store()
        apps = store.get("apps")
        if owner in apps:
            for i, item in enumerate(apps[owner].copy()):
                if repo == item:
                    del apps[owner][i]
                    break
            apps.save()
        store.delete("{}/{}".format(owner, repo))
    return is_success, error


def run(owner, repo):
    root_dir = get_path(owner, repo)
    app_pkg = get_app_pkg(owner, repo)
    if (not app_pkg
            or not root_dir
            or not os.path.exists(root_dir)):
        return False, "This app doesn't exist"
    try:

        p = subprocess.Popen([sys.executable, "-m", app_pkg],
                             cwd=root_dir)
        p.communicate()
    except Exception as e:
        return False, e
    else:
        return True, None


def OLDrollback(owner, repo):
    """
    Rollback. Return boolean is_success, error
    """
    hubstore_apps = _hubstore_apps_folder()
    backup_path = os.path.join(hubstore_apps, "backup")
    backup_owner_path = os.path.join(backup_path, owner)
    backup_repo_path = os.path.join(backup_owner_path, repo)
    hubstore_apps_apps_path = os.path.join(hubstore_apps, "apps",)
    hubstore_apps_owner_path = os.path.join(hubstore_apps_apps_path, owner)
    hubstore_apps_repo = os.path.join(hubstore_apps_owner_path,
                                      "{}-habitat".format(repo))
    if not os.path.exists(backup_repo_path) and os.path.exists(hubstore_apps_repo):
        return False, "There aren't any backup for this app"
    elif not os.path.exists(hubstore_apps_repo):
        return False, "This app doesn't exist"
    if not os.path.exists(hubstore_apps_owner_path):
        try:
            os.mkdir(hubstore_apps_owner_path)
        except Exception as e:
            return False, e
    elif os.path.exists(hubstore_apps_repo):
        cache = os.path.join(constant.PYRUSTIC_DATA, "cache")
        if not os.path.exists(cache):
            try:
                os.makedirs(cache)
            except Exception as e:
                return False, e
        while True:
            random_data = str(uuid.uuid4().hex)
            cache = os.path.join(cache, random_data)
            if not os.path.exists(cache):
                break
        is_success, error = _moveto(hubstore_apps_repo, cache)
        if not is_success:
            return False, error
    return _moveto(backup_repo_path, hubstore_apps_repo)


def get_app_pkg(owner, repo, store=None):
    store = store if store else get_store()
    owner_repo = "{}/{}".format(owner, repo)
    data = store.get(owner_repo)
    app_pkg = data["app_pkg"]
    return app_pkg


def get_path(owner, repo, store=None):
    """
    Use this to get the path to the app owner/repo
    Return a path string or None
    """
    if not store:
        store = get_store()
    if not store:
        return None
    path = os.path.join(store.location,
                        "apps", owner, repo,
                        "habitat")
    if os.path.exists(path):
        return path
    return None


def parse_owner_repo(val):
    data_splitted = val.split("/")
    if len(data_splitted) != 2:
        return None, None
    if data_splitted[0] == "":
        data_splitted[0] = data_splitted[1]
    elif data_splitted[1] == "":
        data_splitted[1] = data_splitted[0]
    owner, repo = data_splitted
    return owner, repo


def get_kurl():
    """
    Generate a Kurl object
    """
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "Pyrustic"}
    return Kurl(headers=headers)


def fetch_latest_release(owner, repo, kurl):
    target = "https://api.github.com"
    url = "{}/repos/{}/{}/releases/latest".format(target, owner, repo)
    response = kurl.request(url)
    json = response.json
    status_code, status_text = response.status
    if status_code == 304:
        json = response.cached_response.json
    return status_code, status_text, json


def fetch_description(owner, repo, kurl):
    target = "https://api.github.com"
    url = "{}/repos/{}/{}".format(target, owner, repo)
    response = kurl.request(url)
    json = response.json
    status_code, status_text = response.status
    if status_code == 304:
        json = response.cached_response.json
    return status_code, status_text, json


def normpath(target, path):
    path = path.lstrip("./\\")
    path = path.rstrip("/\\")
    cache = ""
    parts = []
    for char in path:
        if char in ("/", "\\"):
            parts.append(cache)
            cache = ""
            continue
        cache += char
    parts.append(cache)
    return os.path.join(target, *parts)


def _create_hubstore_apps_folder(parent_path):
    """
    parent_path is the absolute path in which the folder "hubstore-apps"
    will be created.
    return (error, root_dir)
    """
    hubstore_apps = os.path.join(parent_path, "hubstore-apps")
    apps_dir = os.path.join(hubstore_apps, "apps")
    for item in (hubstore_apps, apps_dir):
        if not os.path.exists(item):
            try:
                os.mkdir(item)
            except Exception as e:
                return e, hubstore_apps
    # initialize Store
    store = Store("data", location=hubstore_apps)
    if store.new:
        store.set("apps", dict())
        store.set("favorites", list())
    return None, hubstore_apps


def _register_hubstore_in_pyrustic_data(hubstore_apps):
    location = os.path.join(constant.PYRUSTIC_DATA, "hubstore")
    jason = Jason("meta", location=location)
    jason.data = {"hubstore-apps": hubstore_apps}
    jason.save()


def _install(owner, repo, tempdata):
    """
    Install the cached wheel file
    Return bool is_success, error
    """
    hubstore_apps = get_store().location
    tempdir = tempdata["tempdir"]
    filename = tempdata["filename"]
    src = filename
    dest = os.path.join(hubstore_apps, "apps",
                        owner, repo, "habitat")
    if not os.path.exists(dest):
        os.makedirs(dest)
    try:
        args = ["-m", "pip", "install",
                "--upgrade",
                "--upgrade-strategy", "eager",
                "--target={}".format(dest), src]
        p = subprocess.Popen([sys.executable, *args],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            # pip outputs a warning error about its own version
            # return False, err
            pass
    except Exception as e:
        return False, e
    finally:
        tempdir.cleanup()
    if not os.listdir(dest):
        return False, "Unknown error"
    return True, None


def _moveto(src, dest):
    """
    If the DEST exists:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        - /home/ocean (DEST)
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/lake
        - /home/ocean/lake/fish.txt
    Else IF the DEST doesn't exist:
        * Before moveto *
        - /home/lake (SRC)
        - /home/lake/fish.txt
        * Moveto *
        moveto("/home/lake", "/home/ocean")
        * After Moveto *
        - /home/ocean
        - /home/ocean/fish.txt


    Move a file or directory (src) to a destination folder (dest)
    """
    if not os.path.exists(src):
        return False, None
    try:
        shutil.move(src, dest)
    except Exception as e:
        return False, e
    return True, None
