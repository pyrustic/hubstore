
Back to [Reference Overview](https://github.com/pyrustic/hubstore/blob/master/docs/reference/README.md)

# hubstore.host.core



<br>


```python

def auth(token, kurl):
    """
    Auth
    Return: (status_code, status_text, login_str)
    login_str could be None
    """

```

<br>

```python

def backup(owner, repo):
    """
    Backup the current version of owner/repo
    Return bool is_success, error
    """

```

<br>

```python

def download(owner, repo, name, url, kurl):
    """
    Download the resource (url) with kurl object
    Return a boolean is_success, error, and tempfile
    """

```

<br>

```python

def fetch(owner, repo, kurl):
    """
    Fetch resource
    Param:
        - owner: str
        - repo: str
        - kurl: Kurl object
    
    Return:
        status_code, status_text, json_data
    """

```

<br>

```python

def find_install_script(owner, repo):
    """
    Find the install script
    Return a data dict:
        {"is_success": bool, "error": error, "module": str, "root_dir": str,
        "path": str}
    """

```

<br>

```python

def get_app_pkg(owner, repo):
    """
    
    """

```

<br>

```python

def get_kurl():
    """
    Generate a Kurl object
    """

```

<br>

```python

def get_list():
    """
    Return bool_success, error, data
    Data is the list of apps stored in hubstore-apps
    That list is in reality a dict like:
    {"owner": ["repo_1", "repo_2", ...], "owner_2": [], ...}
    """

```

<br>

```python

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

```

<br>

```python

def install(owner, repo, name):
    """
    Unpack the zip file cached in tempfile.name
    Return bool is_success, error
    """

```

<br>

```python

def parse_owner_repo(val):
    """
    
    """

```

<br>

```python

def path(owner, repo):
    """
    Use this to get the path to the app owner/repo
    Return a path string or None
    """

```

<br>

```python

def rate(kurl):
    """
    Get Rate Limit
    Return: status_code, status_text, data
    data = {"limit": int, "remaining": int}
    """

```

<br>

```python

def rollback(owner, repo):
    """
    Rollback. Return boolean is_success, error
    """

```

<br>

```python

def run(owner, repo):
    """
    
    """

```

<br>

```python

def should_init_hubstore():
    """
    Return a boolean to tell if the method
    "init_HUBSTORE()" should be called or not
    """

```

<br>

```python

def split_arg(arg):
    """
    Split the string arg. Delimiters are space, simple and double quotes
    """

```

<br>

```python

def uninstall(owner, repo):
    """
    Uninstall an app by giving its owner and repo.
    Return bool is_success, error
    """

```

<br>

```python

def useful_info(data):
    """
    Return useful info in a dict. Return None if the dict data is empty 
    """

```

