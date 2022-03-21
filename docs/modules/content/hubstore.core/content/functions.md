Back to [All Modules](https://github.com/pyrustic/hubstore/blob/master/docs/modules/README.md#readme)

# Module Overview

**hubstore.core**
 
No description

> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [OLDrollback](#oldrollback) &nbsp;&nbsp; [\_create\_hubstore\_apps\_folder](#_create_hubstore_apps_folder) &nbsp;&nbsp; [\_install](#_install) &nbsp;&nbsp; [\_moveto](#_moveto) &nbsp;&nbsp; [\_register\_hubstore\_in\_pyrustic\_data](#_register_hubstore_in_pyrustic_data) &nbsp;&nbsp; [app\_metadata](#app_metadata) &nbsp;&nbsp; [backup](#backup) &nbsp;&nbsp; [download](#download) &nbsp;&nbsp; [fetch](#fetch) &nbsp;&nbsp; [fetch\_description](#fetch_description) &nbsp;&nbsp; [fetch\_latest\_release](#fetch_latest_release) &nbsp;&nbsp; [get\_app\_pkg](#get_app_pkg) &nbsp;&nbsp; [get\_kurl](#get_kurl) &nbsp;&nbsp; [get\_path](#get_path) &nbsp;&nbsp; [get\_store](#get_store) &nbsp;&nbsp; [init\_hubstore](#init_hubstore) &nbsp;&nbsp; [install](#install) &nbsp;&nbsp; [normpath](#normpath) &nbsp;&nbsp; [parse\_owner\_repo](#parse_owner_repo) &nbsp;&nbsp; [rate](#rate) &nbsp;&nbsp; [rollback](#rollback) &nbsp;&nbsp; [run](#run) &nbsp;&nbsp; [should\_init\_hubstore](#should_init_hubstore) &nbsp;&nbsp; [uninstall](#uninstall) &nbsp;&nbsp; [useful\_info](#useful_info)
>
> **Constants:** &nbsp; None

# All Functions
[oldrollback](#OLDrollback) &nbsp;&nbsp; [\_create\_hubstore\_apps\_folder](#_create_hubstore_apps_folder) &nbsp;&nbsp; [\_install](#_install) &nbsp;&nbsp; [\_moveto](#_moveto) &nbsp;&nbsp; [\_register\_hubstore\_in\_pyrustic\_data](#_register_hubstore_in_pyrustic_data) &nbsp;&nbsp; [app\_metadata](#app_metadata) &nbsp;&nbsp; [backup](#backup) &nbsp;&nbsp; [download](#download) &nbsp;&nbsp; [fetch](#fetch) &nbsp;&nbsp; [fetch\_description](#fetch_description) &nbsp;&nbsp; [fetch\_latest\_release](#fetch_latest_release) &nbsp;&nbsp; [get\_app\_pkg](#get_app_pkg) &nbsp;&nbsp; [get\_kurl](#get_kurl) &nbsp;&nbsp; [get\_path](#get_path) &nbsp;&nbsp; [get\_store](#get_store) &nbsp;&nbsp; [init\_hubstore](#init_hubstore) &nbsp;&nbsp; [install](#install) &nbsp;&nbsp; [normpath](#normpath) &nbsp;&nbsp; [parse\_owner\_repo](#parse_owner_repo) &nbsp;&nbsp; [rate](#rate) &nbsp;&nbsp; [rollback](#rollback) &nbsp;&nbsp; [run](#run) &nbsp;&nbsp; [should\_init\_hubstore](#should_init_hubstore) &nbsp;&nbsp; [uninstall](#uninstall) &nbsp;&nbsp; [useful\_info](#useful_info)

## OLDrollback
Rollback. Return boolean is_success, error



**Signature:** (owner, repo)





**Return Value:** None.

[Back to Top](#module-overview)


## \_create\_hubstore\_apps\_folder
parent_path is the absolute path in which the folder "hubstore-apps"
will be created.
return (error, root_dir)



**Signature:** (parent\_path)





**Return Value:** None.

[Back to Top](#module-overview)


## \_install
Install the cached wheel file
Return bool is_success, error



**Signature:** (owner, repo, tempdata)





**Return Value:** None.

[Back to Top](#module-overview)


## \_moveto
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



**Signature:** (src, dest)





**Return Value:** None.

[Back to Top](#module-overview)


## \_register\_hubstore\_in\_pyrustic\_data
None



**Signature:** (hubstore\_apps)





**Return Value:** None.

[Back to Top](#module-overview)


## app\_metadata
None



**Signature:** (owner, repo)





**Return Value:** None.

[Back to Top](#module-overview)


## backup
Backup the current version of owner/repo
Return bool is_success, error



**Signature:** (owner, repo)





**Return Value:** None.

[Back to Top](#module-overview)


## download
Download the resource (url) with kurl object
Return a boolean is_success, error, and tempdata
Tempdata: (tempdir, filename)



**Signature:** (name, url, kurl)





**Return Value:** None.

[Back to Top](#module-overview)


## fetch
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



**Signature:** (owner, repo, kurl)





**Return Value:** None.

[Back to Top](#module-overview)


## fetch\_description
None



**Signature:** (owner, repo, kurl)





**Return Value:** None.

[Back to Top](#module-overview)


## fetch\_latest\_release
None



**Signature:** (owner, repo, kurl)





**Return Value:** None.

[Back to Top](#module-overview)


## get\_app\_pkg
None



**Signature:** (owner, repo, store=None)





**Return Value:** None.

[Back to Top](#module-overview)


## get\_kurl
Generate a Kurl object



**Signature:** ()





**Return Value:** None.

[Back to Top](#module-overview)


## get\_path
Use this to get the path to the app owner/repo
Return a path string or None



**Signature:** (owner, repo, store=None)





**Return Value:** None.

[Back to Top](#module-overview)


## get\_store
Returns the main store datastore if it exists,
else returns None



**Signature:** ()





**Return Value:** None.

[Back to Top](#module-overview)


## init\_hubstore
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
        - data: this is where the library Dossier stores data.



**Signature:** (path)





**Return Value:** None.

[Back to Top](#module-overview)


## install
Install the cached wheel file
Return bool is_success, error



**Signature:** (owner, repo, name, tempdata)





**Return Value:** None.

[Back to Top](#module-overview)


## normpath
None



**Signature:** (target, path)





**Return Value:** None.

[Back to Top](#module-overview)


## parse\_owner\_repo
None



**Signature:** (val)





**Return Value:** None.

[Back to Top](#module-overview)


## rate
Get Rate Limit
Return: status_code, status_text, data
data = {"limit": int, "remaining": int}



**Signature:** (kurl)





**Return Value:** None.

[Back to Top](#module-overview)


## rollback
Rollback. Return boolean is_success, error



**Signature:** (owner, repo)





**Return Value:** None.

[Back to Top](#module-overview)


## run
None



**Signature:** (owner, repo)





**Return Value:** None.

[Back to Top](#module-overview)


## should\_init\_hubstore
None



**Signature:** ()





**Return Value:** None.

[Back to Top](#module-overview)


## uninstall
Uninstall an app by providing its owner and repo.
Return bool is_success, error



**Signature:** (owner, repo)





**Return Value:** None.

[Back to Top](#module-overview)


## useful\_info
Return useful info in a dict. Return None if the dict data is empty 



**Signature:** (data)





**Return Value:** None.

[Back to Top](#module-overview)


