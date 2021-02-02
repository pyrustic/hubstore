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
`Hubstore` is a lightweight software that allows you to download, store, and run `Python` `desktop applications`.

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
`Hubstore` is built to allow end-users to easily download, install, and use applications published with the help of `Pyrustic`.

`Hubstore` itself is built with the `Pyrustic` framework and is available on PyPI.

As a developer, you simply need to publish a new release of your application with [Pyrustic](https://github.com/pyrustic/pyrustic#readme) to make it compatible with `Hubstore`.

An application is compatible with `Hubstore`:
- if it is available as a zip asset in Github Release;
- unpacking the zip asset should output a folder named as the Github repository;
- a `main.py` module should be present in the root of the project (inside the folder named as the Github repository).

This is a beta version of `Hubstore`, so it's recommended to be a curious hacker and play with a [demo](https://github.com/pyrustic/pyrustic#tutorial) project.

As an end-user, you just need to know the repository name and owner to download an app via `Hubstore`: {owner}/{repo}. You can also simply paste the url of the project repository.

The repository [hubstore-apps](https://github.com/pyrustic/hubstore-apps) will store a curated list of `Hubstore` compatible apps. Therefore, if you like this project and/or want to make your app available via `Hubstore`, you know what to do :-)

<!-- Demo -->
## Demo
<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore_demo_1.gif" alt="Hubstore First Time" width="650">
    <p align="center">
    Using Hubstore for the first time. You can reproduce it as it.
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
$ pip install hubstore
$ hubstore
```

<!-- License -->
## License
`Pyrustic` is licensed under the terms of the permissive free software license `MIT License`.

<!-- Contact -->
## Contact
Hi ! I'm Alex, operating by ["Crocker's Rules"](http://sl4.org/crocker.html)
<!-- Image -->
![email](https://raw.githubusercontent.com/pyrustic/misc/master/media/email.png)

