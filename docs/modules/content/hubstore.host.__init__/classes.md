Back to [Modules overview](https://github.com/pyrustic/hubstore/blob/master/docs/modules/README.md)
  
# Module documentation
>## hubstore.host.\_\_init\_\_
No description
<br>
[classes (2)](https://github.com/pyrustic/hubstore/blob/master/docs/modules/content/hubstore.host.__init__/classes.md)


## Classes
```python
class Data(object):
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

```python
class Host(object):
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

    def _get_process(self, process_id):
        """
        
        """

    def _on_app_exit(self, error, process_id):
        """
        
        """

    def _run(self, owner, repo, process_id):
        """
        
        """

    def _search_offline(self, owner, repo):
        """
        
        """

    def _search_online(self, owner, repo):
        """
        
        """

    def _setup(self):
        """
        
        """

    def _show_promoted(self):
        """
        
        """

    def _update_app_info(self, owner, repo):
        """
        
        """

    def _update_quota(self):
        """
        
        """

```

