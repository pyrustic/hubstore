import os.path
from hubstore import about as hubstore_about


#
USER_AGENT = ("User-Agent", "Pyrustic")

#
PYRUSTIC_DATA = os.path.join(os.path.expanduser("~"), "PyrusticData")

#
HUBSTORE_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA, "hubstore")
HUBSTORE_SHARED_DATA_FILE = os.path.join(HUBSTORE_SHARED_FOLDER,
                                         "hubstore_shared_data.json")
DEFAULT_HUBSTORE_SHARED_DATA_FILE = os.path.join(hubstore_about.ROOT_DIR,
                                                 "misc", "default_json",
                                                 "default_shared_data.json")
DEFAULT_HUBSTORE_APPS_LIST_FILE = os.path.join(hubstore_about.ROOT_DIR,
                                               "misc", "default_json",
                                               "default_apps_list_data.json")
#
ABOUT_JSON_FILE = os.path.join(hubstore_about.ROOT_DIR,
                               "pyrustic_data", "about.json")

#
