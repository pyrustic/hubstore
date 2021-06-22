
Back to [Reference Overview](https://github.com/pyrustic/hubstore/blob/master/docs/reference/README.md)

# hubstore.host.main\_host



<br>


```python

class MainHost:
    """
    
    """

    def __init__(self):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    @property
    def login(self):
        """
        
        """

    def auth(self, token):
        """
        Return: (status_code, status_text, login_str)
        data = the login if status is 200 or 304, else data is None
        """

    def download(self, name, url, owner, repo):
        """
        Return {"success": bool, "error": object}
        """

    def get_image(self, owner, repo):
        """
        Return None or path
        """

    def get_info(self, owner, repo):
        """
        Return None or data.
        data:
            {"owner": str, "repo": str,
             "path": str, "email": str,
             "version": str,
             "description": str,
             "homepage": str}
        """

    def get_list(self):
        """
        Return success_bool, error, data
        Data is the list of apps like this:
            [ ("owner_1", "repo_1"), ("owner_2", "repo_2"),
              ("owner_3", "repo_3"), ("owner_4", "repo_4") ]
        """

    def get_rate(self):
        """
        Get Rate Limit
        Return:
             {"status_code": int, "status_text": str,
              "data": data}
        data = {"limit": int, "remaining": int}
        """

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

    def parse_owner_repo(self, val):
        """
        Param:
            val: string
        Return:
            A tuple of strings as ("owner", "repo")
            or a tuple of None as (None, None)
        """

    def rollback(self, owner, repo):
        """
        Rollback. Return boolean is_success, error 
        """

    def run(self, owner, repo, callback_process_id):
        """
        
        """

    def search_offline(self, owner, repo):
        """
        Param
            owner and repo are strings
        Return
            Boolean.
        """

    def search_online(self, owner, repo):
        """
        Return:
        {"success": bool,
                "status": tuple(status_code, status_text),
                "release": dict of useful data,
                "assets": list of dicts}
        """

    def should_init_hubstore(self):
        """
        Return a boolean to tell if the method
        "init_hubstore()" should be called or not
        """

    def stop_process(self, process_id):
        """
        
        """

    def unauth(self):
        """
        
        """

    def uninstall(self, owner, repo):
        """
        Delete an app by giving its owner and repo.
        Return bool is_success, error
        """

```

