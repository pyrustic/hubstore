import os
import os.path
import uuid
import shutil
import subprocess
import sys
from hubstore.host import constants
from pyrustic.jasonix import Jasonix
from pyrustic.gurl import Gurl
from tempfile import TemporaryDirectory


def should_init_hubstore():
    """
    Return a boolean to tell if the method
    "init_HUBSTORE()" should be called or not
    """
    if not os.path.exists(constants.HUBSTORE_SHARED_DATA_FILE):
        return True
    hubstore_apps = _hubstore_apps_folder()
    if hubstore_apps is None:
        return True
    if not os.path.exists(hubstore_apps):
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
            2 = failed to register Hubstore in $HOME/PyrusticData
        - "root_dir" is the absolute path to the folder "hubstore-apps".
        Example: init_hubstore("/path/to/use") will return this "root_dir":
            "/path/to/use/hubstore-apps"
        Inside "hubstore-apps", two main folders:
            - apps: to store apps by owner. Meaning that visible folders
            in "apps" are owners, and inside each owner there are a repo
            - backup: it mirrors the folder "apps" but only for backup.
        And one JSON file: apps.json to store the owners/repos associations
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
    error = _register_hubstore_in_pyrustic_data(root_dir)
    if error is not None:
        data["error_code"] = 2
        data["error"] = error
        return data
    data["root_dir"] = root_dir
    return data


def rate(gurl):
    """
    Get Rate Limit
    Return: status_code, status_text, data
    data = {"limit": int, "remaining": int}
    """
    target = "https://api.github.com"
    url = "{}/rate_limit".format(target)
    response = gurl.request(url)
    json = response.json
    status_code, status_text = response.status
    data = {}
    if status_code == 304:
        data = response.cached_response.json
    if (status_code in (200, 304)) and json:
        data["limit"] = json["resources"]["core"]["limit"]
        data["remaining"] = json["resources"]["core"]["remaining"]
    return status_code, status_text, data


def auth(token, gurl):
    """
    Auth
    Return: (status_code, status_text, login_str)
    login_str could be None
    """
    target = "https://api.github.com"
    url = "{}/user".format(target)
    gurl.token = token
    response = gurl.request(url)
    json = response.json
    status_code, status_text = response.status
    data = None
    if status_code == 304:
        json = response.cached_response.json
    if (status_code in (200, 304)) and json:
        data = json["login"]
    return status_code, status_text, data


def fetch(owner, repo, gurl):
    """ Fetch resource
    Param:
        - owner: str
        - repo: str
        - gurl: Gurl object

    Return:
        status_code, status_text, json_data
    """
    target = "https://api.github.com"
    url = "{}/repos/{}/{}/releases/latest".format(target, owner, repo)
    response = gurl.request(url)
    json = response.json
    status_code, status_text = response.status
    if status_code == 304:
        json = response.cached_response.json
    return status_code, status_text, json


def useful_info(data):
    """ Return useful info in a dict. Return None if the dict data is empty """
    if not data:
        return None
    info = {"tag_name": data["tag_name"],
            "target_commitish": data["target_commitish"],
            "created_at": _badass_iso_8601_date_parser(data["created_at"]),
            "published_at": _badass_iso_8601_date_parser(data["published_at"]),
            "author_login": data["author"]["login"],
            "assets": []}
    for asset in data["assets"]:
        cache = {"name": asset["name"],
                 "size": asset["size"],
                 "url": asset["browser_download_url"],
                 "created_at": _badass_iso_8601_date_parser(asset["created_at"]),
                 "updated_at": _badass_iso_8601_date_parser(asset["updated_at"]),
                 "uploader_login": asset["uploader"]["login"],
                 "download_count": asset["download_count"],
                 "content_type": asset["content_type"]}
        info["assets"].append(cache)
    return info


def download(name, url, gurl):
    """
    Download the resource (url) with gurl object
    Return a boolean is_success, error, and tempfile
    """
    is_success = True
    error = None
    tempfile = TemporaryDirectory()
    cache_path = tempfile.name
    cached_zip = os.path.join(cache_path, name)
    response = gurl.request(url)
    data = response.body
    if response.code == 304:
        if response.cached_response:
            data = response.cached_response.body
    if data is None:
        return None, "The server returned an empty body", None, name
    try:
        with open(cached_zip, "wb") as file:
            file.write(data)
    except Exception as e:
        error = e
        is_success = False
        tempfile.cleanup()
        tempfile = None
    return is_success, error, tempfile, name


def backup(owner, repo):
    """
    Backup the current version of owner/repo
    Return bool is_success, error
    """
    is_success = True
    error = None
    hubstore_apps = _hubstore_apps_folder()
    hubstore_apps_owner = os.path.join(hubstore_apps, "apps", owner)
    hubstore_apps_repo = os.path.join(hubstore_apps_owner, repo)
    if not os.path.exists(hubstore_apps_repo):
        return False, None
    backup_path = os.path.join(hubstore_apps, "backup")
    backup_owner_path = os.path.join(backup_path, owner)
    backup_repo_path = os.path.join(backup_owner_path, repo)
    if not os.path.exists(backup_owner_path):
        try:
            os.mkdir(backup_owner_path)
        except Exception as e:
            return False, e
    elif os.path.exists(backup_repo_path):
        cache = os.path.join(constants.PYRUSTIC_DATA, "cache")
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
        cache = _moveto(backup_path, cache)
        if not cache[0]:
            return False, True
    src = hubstore_apps_repo
    dest = backup_repo_path
    if os.path.exists(src):
        is_success, error = _moveto(src, dest)
    return is_success, error


def unpack(name, tempfile, owner, repo):
    """
    Unpack the zip file cached in tempfile.name
    Return bool is_success, error
    """
    hubstore_apps = _hubstore_apps_folder()
    src = os.path.join(tempfile.name, name)
    dest = os.path.join(hubstore_apps, "apps", owner)
    try:
        shutil.unpack_archive(src, dest)
    except Exception as e:
        return False, e
    finally:
        tempfile.cleanup()
    # register app in apps.json
    cache = constants.DEFAULT_HUBSTORE_APPS_LIST_FILE
    jasonix = Jasonix(os.path.join(hubstore_apps, "apps.json"),
                      default=cache)
    if owner in jasonix.data:
        if repo not in jasonix.data[owner]:
            jasonix.data[owner].append(repo)
    else:
        jasonix.data[owner] = [repo]
    jasonix.save()
    return True, None


def find_install_script(owner, repo):
    """
    Find the install script
    Return a data dict:
        {"is_success": bool, "error": error, "module": str, "root_dir": str,
        "path": str}
    """
    response = {"is_success": True,
                "error": None,
                "module": None,
                "root_dir": None,
                "path": None}
    hubstore_apps = _hubstore_apps_folder()
    root_dir = os.path.join(hubstore_apps, "apps", owner, repo)
    if not os.path.exists(root_dir):
        response["is_success"] = False
        response["error"] = "This app doesn't exist"
        return response
    # == Find install script in pyrustic_data folder in the root_dir
    data = _search_install_script_in_pyrustic_data(root_dir)
    is_success, error, module = data
    if is_success:
        path = _convert_module_to_path(root_dir, module)
        response["module"] = module
        response["root_dir"] = root_dir
        response["path"] = path
        if not os.path.exists(path):
            response["is_success"] = False
            response["error"] = "Missing install script"
        return response
    elif not is_success and error is not None:
        response["is_success"] = False
        response["error"] = error
        return response
    # == Find install.py
    path = os.path.join(root_dir,
                        "install.py")
    if os.path.exists(path):
        response["module"] = "install"
        response["root_dir"] = root_dir
        response["path"] = path
        return response
    response["is_success"] = False
    return response


def get_list():
    """
    Return bool_success, error, data
    Data is the list of apps stored in hubstore-apps
    That list is in reality a dict like:
    {"owner": ["repo_1", "repo_2", ...], "owner_2": [], ...}
    """
    hubstore_apps = _hubstore_apps_folder()
    apps_json = os.path.join(hubstore_apps, "apps.json")
    data = None
    try:
        jasonix = Jasonix(apps_json,
                          default=constants.DEFAULT_HUBSTORE_APPS_LIST_FILE)
        data = jasonix.data
    except Exception as e:
        return False, e, data
    return True, None, data


def uninstall(owner, repo):
    """
    Uninstall an app by giving its owner and repo.
    Return bool is_success, error
    """
    is_success = None
    error = None
    hubstore_apps = _hubstore_apps_folder()
    apps_data = os.path.join(hubstore_apps, "apps.json")
    jasonix = Jasonix(apps_data, default=constants.DEFAULT_HUBSTORE_APPS_LIST_FILE)
    root_dir = os.path.join(hubstore_apps, "apps", owner, repo)
    try:
        repos = jasonix.data[owner]
        index = None
        for i, item in enumerate(repos):
            if item == repo:
                index = i
                break
        del jasonix.data[owner][index]
        jasonix.save()
    except KeyError as e:
        error = "Unknown owner"
    except (IndexError, TypeError) as e:
        is_success = False
        error = "Unknown repo"
    except Exception as e:
        is_success = False
        error = e
    else:
        is_success, error = backup(owner, repo)
    return is_success, error

def run(owner, repo):
    hubstore_apps = _hubstore_apps_folder()
    root_dir = os.path.join(hubstore_apps, "apps", owner, repo)
    if os.path.exists(root_dir):
        try:
            p = subprocess.Popen([sys.executable, "."],
                                 cwd=root_dir)
            p.communicate()
        except Exception as e:
            return False, e
        else:
            return True, None
    else:
        return False, "This app doesn't exist"


def rollback(owner, repo):
    """
    Rollback. Return boolean is_success, error
    """
    hubstore_apps = _hubstore_apps_folder()
    backup_path = os.path.join(hubstore_apps, "backup")
    backup_owner_path = os.path.join(backup_path, owner)
    backup_repo_path = os.path.join(backup_owner_path, repo)
    hubstore_apps_apps_path = os.path.join(hubstore_apps, "apps",)
    hubstore_apps_owner_path = os.path.join(hubstore_apps_apps_path, owner)
    hubstore_apps_repo = os.path.join(hubstore_apps_owner_path, repo)
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
        cache = os.path.join(constants.PYRUSTIC_DATA, "cache")
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


def path(owner, repo):
    """
    Use this to get the path to the app owner/repo
    Return a path string or None
    """
    hubstore_apps = _hubstore_apps_folder()
    hubstore_apps_owner = os.path.join(hubstore_apps, "apps", owner)
    hubstore_apps_repo = os.path.join(hubstore_apps_owner, repo)
    if not os.path.exists(hubstore_apps_repo):
        hubstore_apps_repo = None
    return hubstore_apps_repo


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


def split_arg(arg):
    """
    Split the string arg. Delimiters are space, simple and double quotes
    """
    args = []
    cache = ""
    simple_quote_on = False
    double_quote_on = False
    collect_cache = False
    for char in arg:
        # Quotes stuff
        if char == "'":  # simple quote
            collect_cache = True
            simple_quote_on = False if simple_quote_on else True
        elif char == '"':  # double quote
            collect_cache = True
            double_quote_on = False if double_quote_on else True
        # space stuff
        elif char == " " and (not simple_quote_on and not double_quote_on):
            collect_cache = True
        else:
            cache += char
        # caching
        if collect_cache:
            collect_cache = False
            if cache:
                args.append(cache)
                cache = ""
    if cache:
        args.append(cache)
    return args


def get_gurl():
    """
    Generate a Gurl object
    """
    headers = {"Accept": "application/vnd.github.v3+json",
               "User-Agent": "Pyrustic"}
    gurl = Gurl(headers=headers)
    return gurl


# ======================================
#               PRIVATE
# ======================================
def _create_hubstore_apps_folder(parent_path):
    """
    parent_path is the absolute path in which the folder "hubstore-apps"
    will be created.
    return (error, root_dir)
    """
    hubstore_apps = os.path.join(parent_path, "hubstore-apps")
    apps_dir = os.path.join(hubstore_apps, "apps")
    backup_dir = os.path.join(hubstore_apps, "backup")
    for item in (hubstore_apps, apps_dir, backup_dir):
        if not os.path.exists(item):
            try:
                os.mkdir(item)
            except Exception as e:
                return e, hubstore_apps
    try:
        Jasonix(os.path.join(hubstore_apps, "apps.json"),
                constants.DEFAULT_HUBSTORE_APPS_LIST_FILE)
    except Exception as e:
        return e, hubstore_apps
    return None, hubstore_apps


def _register_hubstore_in_pyrustic_data(hubstore_apps):
    """ Return error or None """
    PYRUSTIC_DATA = constants.PYRUSTIC_DATA
    HUBSTORE_SHARED_FOLDER = constants.HUBSTORE_SHARED_FOLDER
    HUBSTORE_SHARED_DATA_FILE = constants.HUBSTORE_SHARED_DATA_FILE
    DEFAULT_HUBSTORE_SHARED_DATA_FILE = constants.DEFAULT_HUBSTORE_SHARED_DATA_FILE
    for item in (PYRUSTIC_DATA, HUBSTORE_SHARED_FOLDER):
        if not os.path.exists(item):
            try:
                os.mkdir(item)
            except Exception as e:
                return e
    # JSON
    try:
        jasonix = Jasonix(HUBSTORE_SHARED_DATA_FILE,
                          default=DEFAULT_HUBSTORE_SHARED_DATA_FILE)
        jasonix.data["hubstore-apps"] = hubstore_apps
        jasonix.save()
    except Exception as e:
        return e
    return None


def _badass_iso_8601_date_parser(date):
    # YYYY-MM-DDTHH:MM:SSZ
    date = date.rstrip("Z")
    date_part, time_part = date.split("T")
    months = ("Jan", "Feb", "March", "April", "May", "June", "July",
              "Aug", "Sept", "Oct", "Nov", "Dec")
    year, month, day = date_part.split("-")
    text = "{} {} {} at {}".format(day, months[int(month) - 1], year, time_part)
    return text


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
    if not os.path.exists(src) or os.path.exists(dest):
        return False, None
    try:
        shutil.move(src, dest)
    except Exception as e:
        return False, e
    return True, None


def _hubstore_apps_folder():
    jasonix = Jasonix(constants.HUBSTORE_SHARED_DATA_FILE)
    hubstore_apps = jasonix.data.get("hubstore-apps")
    return hubstore_apps


def _search_install_script_in_pyrustic_data(root_dir):
    about_json = os.path.join(root_dir, "pyrustic_data", "about.json")
    if os.path.exists(about_json):
        try:
            jasonix = Jasonix(about_json)
            module = jasonix.data.get("install_script", None)
        except Exception as e:
            return False, e, None
        else:
            if module is None:
                return False, None, None
            else:
                return True, None, module
    return False, None, None


def _convert_module_to_path(root_dir, dotted_path):
    dotted_path_splitted = dotted_path.split(".")
    path = os.path.join(root_dir, *dotted_path_splitted)
    path = "{}.py".format(path)
    return path


def _path_to_owner_repo(owner, repo):
    hubstore_apps = _hubstore_apps_folder()
    return os.path.join(hubstore_apps, owner, repo)
