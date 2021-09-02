
Back to [Reference Overview](https://github.com/pyrustic/hubstore/blob/master/docs/reference/README.md#readme)

# hubstore.core.\_\_init\_\_



<br>


```python

def OLDrollback(owner, repo):
    """
    Rollback. Return boolean is_success, error
    """

```

<br>

```python

def app_metadata(owner, repo):
    """
    
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

def download(name, url, kurl):
    """
    Download the resource (url) with kurl object
    Return a boolean is_success, error, and tempdata
    Tempdata: (tempdir, filename)
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
        Json_data: {"description": str, "stargazers": int,
                    "tag": str, "published_at": str,
                    "downloads": int, "size": int,
                    "repository": str, "owner_repo": str,
                    "assets": list}
    """

```

<br>

```python

def fetch_description(owner, repo, kurl):
    """
    
    """

```

<br>

```python

def fetch_latest_release(owner, repo, kurl):
    """
    
    """

```

<br>

```python

def get_app_pkg(owner, repo, store=None):
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

def get_path(owner, repo, store=None):
    """
    Use this to get the path to the app owner/repo
    Return a path string or None
    """

```

<br>

```python

def get_store():
    """
    Returns the main store datastore if it exists,
    else returns None
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
        - "root_dir" is the absolute path to the folder "hubstore-apps".
        Example: init_hubstore("/path/to/use") will return this "root_dir":
            "/path/to/use/hubstore-apps"
        Inside "hubstore-apps", two main folders:
            - apps: to store apps by owner. Meaning that visible folders
            in "apps" are owners, and inside each owner there are a repo
            - data: this is where the library Store stores data.
    """

```

<br>

```python

def install(owner, repo, name, tempdata):
    """
    Install the cached wheel file
    Return bool is_success, error
    """

```

<br>

```python

def normpath(target, path):
    """
    
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
    
    """

```

<br>

```python

def uninstall(owner, repo):
    """
    Uninstall an app by providing its owner and repo.
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

