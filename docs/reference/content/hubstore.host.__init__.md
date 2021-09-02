
Back to [Reference Overview](https://github.com/pyrustic/hubstore/blob/master/docs/reference/README.md#readme)

# hubstore.host.\_\_init\_\_



<br>


```python

class Data:
    """
    
    """

    def __init__(self, host):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    @property
    def store(self):
        """
        
        """

    def get_all_apps(self):
        """
        
        """

    def get_apps_directory(self):
        """
        
        """

    def get_cover_image(self):
        """
        
        """

    def get_default_cover_image(self):
        """
        
        """

    def get_default_image(self):
        """
        
        """

    def get_favorites_apps(self):
        """
        
        """

    def get_image(self, owner, repo):
        """
        
        """

```

<br>

```python

class Host:
    """
    
    """

    def __init__(self, main_view):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    @property
    def data(self):
        """
        
        """

    @property
    def initialized(self):
        """
        
        """

    @property
    def threadom(self):
        """
        
        """

    def close_app(self, process_id):
        """
        
        """

    def favorite(self, owner_repo, val=True):
        """
        
        """

    def install(self, owner, repo, name, url):
        """
        
        """

    def on_start_app(self):
        """
        
        """

    def open_website(self, url):
        """
        
        """

    def rollback(self, owner, repo):
        """
        
        """

    def run_app(self, owner, repo):
        """
        
        """

    def search(self, owner, repo):
        """
        
        """

    def show_about(self):
        """
        
        """

    def show_all_apps(self):
        """
        
        """

    def show_app_info(self, owner, repo):
        """
        
        """

    def show_apps_from(self, owner):
        """
        
        """

    def show_favorite_apps(self):
        """
        
        """

    def show_open(self):
        """
        
        """

    def show_promoted(self):
        """
        
        """

    def submit_apps_directory(self, path):
        """
        
        """

    def uninstall(self, owner, repo):
        """
        
        """

    def update(self, owner, repo):
        """
        
        """

```

