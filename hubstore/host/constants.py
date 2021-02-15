import os.path


#
USER_AGENT = ("User-Agent", "Pyrustic")

#
PYRUSTIC_DATA = os.path.join(os.path.expanduser("~"), "PyrusticData")

#
HUBSTORE_SHARED_FOLDER = os.path.join(PYRUSTIC_DATA, "hubstore")
HUBSTORE_SHARED_DATA_FILE = os.path.join(HUBSTORE_SHARED_FOLDER,
                                         "hubstore_shared_data.json")
