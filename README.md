
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore_cover.png" alt="Hubstore Cover">
    <br>
    <p align="center">
    Hubstore - built with Pyrustic
    </p>
</div>

<!-- Intro Text -->
# Hubstore
`Hubstore` is a lightweight software that allows you to download, install, manage, and run `Python` `desktop applications`.

This is an [emailware](https://en.wiktionary.org/wiki/emailware). You are encouraged to send a [feedback](#contact).

<!-- Quick Links -->
[Demo](#demo) | [Features](#features) | [Installation](#installation)

<!-- Table of contents -->
## Table Of Contents
- [Overview](#overview)
- [Demo](#demo)
- [Philosophy](#philosophy)
- [Features](#features)
- [Installation](#installation)
- [License](#license)
- [Contact](#contact)

<!-- Overview -->
## Overview
Once you have developed a Python desktop application with or without [Pyrustic](https://github.com/pyrustic/pyrustic#readme), the next goal is to distribute it to end-users.

You can use `Pyrustic` to build the distribution package (Wheel) and then publish your application on Github with the `Pyrustic` tool `Hubway`.

You can still ignore `Pyrustic` and use your favorite tools to build a Wheel then release it as an asset on Github.

Now imagine a modern lightweight desktop application where end-users could simply type your Github profile name slash your repository name (Example: pyrustic/demo) or simply paste your repository URL (Example: https://github.com/pyrustic/demo).

End-users will then just click a button to get the latest version of the built distribution (Wheel) of your project and then decide to install it.

This modern lightweight desktop application exists: `Hubstore`.

What else end-users could do ? Well, they can update the previously installed app, rollback to a previous version (because the latest release sucks ! and yes `Hubstore` makes backup duh !), uninstall apps (with its dependencies !), open more than one apps with the possibility of closing them from the `Hubstore` taskbar. And guess what, end-users don't have to think about your application's dependencies because `Hubstore` takes care of these details and end-users aren't probably even programmers !

`Hubstore` will assign a beautiful default image to your app once it is installed. As a software producer, you can control this detail and some others details like `requirements.txt` you would expect the end-users to `pip install`, or the script you would like `Hubstore` to execute at installation and/or uninstallation. It is easy to configure these details, just open the command-line tool Pyrustic `Manager`, issue the command `init` (yes even in existing project, it shouldn't break it, but you know this is still Beta, so... ;-), go inside the JSON file `hubstore.json` in the folder `$APP_DIR/pyrustic_data`, change the values, build a Wheel, publish a new release on Github, done ! So easy !

`Hubstore` is built with the `Pyrustic` framework and is available on PyPI. As `Hubstore` consumes Python standard package format `Wheel`, it is compatible with lot of existing projects.

Only three constraints:
- you have to follow the conventional Python project structure as described in the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/);
- you need to have a `__main__.py` file in the source package;
- the project name should be the same as the source package.

In fact, these aren't constraints but simply `elegance` and [proactivity](https://en.wikipedia.org/wiki/Proactivity). It will save you a lot of trouble in the future (believe me). By the way, the Pyrustic command-line tool `Manager` will take care of these details for you, you will just need to link a project directory, then issue the command `init`. `Manager` can be used programmatically and is an optional tool.


This is a beta version of `Hubstore`, so it's recommended to be a curious hacker and play with a [demo](https://github.com/pyrustic/pyrustic#tutorial) project.


The repository [hubstore-apps](https://github.com/pyrustic/hubstore-apps) will store a curated list of `Hubstore` trendy compatible apps. Therefore, if you like this project and/or want to showcase your app, you know what to do :-)

<!-- Demo -->
## Demo
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore_demo_1.gif" alt="Hubstore First Time" width="650">
    <p align="center">
    Using Hubstore for the first time. You can really reproduce it as it.
    </p>
</div>

<br>
<br>

<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore_demo_2.gif" alt="Hubstore Fictional" width="650">
    <p align="center">
    This is obviously fictional
    </p>
</div>


<!-- Philosophy -->
## Philosophy
### Wisdom from Antiquity
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/diogenes.jpg" alt="Diogenes" width="650">
    <p align="center">
    By <a href="https://en.wikipedia.org/wiki/en:Jean-L%C3%A9on_G%C3%A9r%C3%B4me" class="extiw" title="w:en:Jean-Léon Gérôme">Jean-Léon Gérôme</a> - <a href="https://en.wikipedia.org/wiki/en:Walters_Art_Museum" class="extiw" title="w:en:Walters Art Museum">Walters Art Museum</a>: <a href="https://thewalters.org/" rel="nofollow"></a> <a rel="nofollow" class="external text" href="https://thewalters.org/">Home page</a>&nbsp;<a href="https://art.thewalters.org/detail/31957" rel="nofollow"></a> <a rel="nofollow" class="external text" href="https://art.thewalters.org/detail/31957">Info about artwork</a>, Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=323523">Link</a>
    </p>
</div>

<br>

> He owned a cup which served also as a bowl for food but threw it away when he saw a boy drinking water from his hands and realized one did not even need a cup to sustain oneself.</p>
>
>    --Mark, J. J. (2014, August 02). [Diogenes of Sinope](href="https://www.ancient.eu/Diogenes_of_Sinope/). Ancient History Encyclopedia. Retrieved from https://www.ancient.eu/Diogenes_of_Sinope/

<br>

### Advertisement from the twentieth century
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/ibm.jpg" alt="IBM" width="650">
    <p align="justify">
    By Cecile &amp; Presbrey advertising agency for International Business Machines. - Scanned from the December 1951 issue of Fortune by <a href="//commons.wikimedia.org/wiki/User:Swtpc6800" title="User:Swtpc6800">User:Swtpc6800</a> Michael Holley. The image was touched up with Adobe Photo Elements., Public Domain, <a href="https://commons.wikimedia.org/w/index.php?curid=17480483">Link</a>
    </p>
</div>


<!-- Features -->
## Features
You can export and import a list of apps. You can auth yourself with your Github personal access token to increase the API rate limit.
It is easy to generate a personal access token. Read this [article](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).

You can update your apps, and even rollback to the previous version if the update is buggy.

Play with `Hubstore` to discover more about it.



<!-- Installation -->
## Installation
`Hubstore` is available on [PyPI](https://pypi.org/) (the Python Package Index) to simplify the life of Python developers.

If you have never installed a package from PyPI, you must install the pip tool enabling you to download and install a PyPI package. There are several methods which are described on this [page](https://pip.pypa.io/en/latest/installing/).


```bash
$ pip install hubstore --upgrade --upgrade-strategy eager
```

I recommend you to try the demo: just type `pyrustic/demo` in `Hubstore`. You can go to check the demo code source, it has a conventional Python project structure, there are not any voodoo magic. You can alter the __main__.py file and put there a dumb Tkinter calc code, build the project with your favorite tool or with `Pyrustic Manager`, publish it on Github, then update the previous installed version via `Hubstore`. By the way, `Hubstore` doesn't mess with sys.path or any environment variable. It is fully cross platform, and it doesn't use any virtual environment tool, just the good old vanilla Python ;)

`Hubstore` simply take profit of the elegance of Python itself to avoid platform-specific scripts/stuff/voodoo. 




<!-- License -->
## License
`Pyrustic` is licensed under the terms of the permissive free software license `MIT License`.

<!-- Contact -->
## Contact
Hi ! I'm Alex, operating by ["Crocker's Rules"](http://sl4.org/crocker.html)
<!-- Image -->
![email](https://raw.githubusercontent.com/pyrustic/misc/master/media/email.png)

