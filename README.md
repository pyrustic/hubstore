<!-- Image -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/ecosystem.png" alt="Hubstore Cover">
    <br>
    <p align="center">
    Overview of the Pyrustic Open Ecosystem
    </p>
</div>

<!-- Intro Text -->
# Hubstore
<b>  Distribute, promote, discover, install, and run Python desktop applications  </b>

This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).

<!-- Quick Links -->
[Installation](#installation) | [User side](#user-side) | [Developer side](#developer-side) | [Demo](#demo)



## Overview
`Hubstore` allows software developers to distribute their apps to users through [Github](https://github.com/about).

Let's visit both sides of the distribution pipeline.

### User side
Let's discover Hubstore through a series of screenshots

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-empty.png" alt="Figure" width="800">
    <p align="center">
    <i> A minimalist, clean and elegant graphical user interface </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-app-installer.png" alt="Figure" width="800">
    <p align="center">
    <i> Type developer/app-name in the search bar to install an app </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-app-info.png" alt="Figure" width="800">
    <p align="center">
    <i> You can rollback to the previously installed version of an app </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-autocomplete.png" alt="Figure" width="800">
    <p align="center">
    <i> Hubstore uses <a href="https://github.com/pyrustic/suggestion">Suggestion</a> to implement the autocomplete feature </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-apps-running.png" alt="Figure" width="800">
    <p align="center">
    <i> Install apps, run apps, and close apps from the same interface </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-promoted.png" alt="Figure" width="800">
    <p align="center">
    <i> Discover new apps through the Promoted feature </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/hubstore-bug-report.png" alt="Figure" width="800">
    <p align="center">
    <i> Built-in bug reporting system to allow users to help improve the apps </i>
    </p>
</div>

<br>


### Developer side
Once you have developed a Python desktop application with or without [Pyrustic Framework](https://github.com/pyrustic/pyrustic#readme), the next goal is to distribute it to end users.

Suppose you already have a Github profile and have already created a repository named as your project name.

To allow users to access your apps through Hubstore, you need to publish your app's distribution package (Wheel) on Github. Concretely, it is a question of doing this:
- test your project;
- create the distribution package (Wheel) of your application (the project must have a `__main__.py` entry point);
- create a `Release` on Github;
- upload the `Wheel` file of your application as a `Release asset`.

You can use the [Backstage](https://github.com/pyrustic/backstage) project management tool's `build` and `release` commands, respectively, to automate these steps. `Backstage` also manages the versioning of your project.

Then, the user just has to copy and paste the URL of your project's repository into `Hubstore`.

`Hubstore` assigns a default nice image to your app. You can modify the image by editing the configuration file `$APP_DIR/pyrustic_data/hubstore/img.json`. The image must have the following characteristics: `200x80 .PNG`

To `promote` other apps of which you are the author or friend of the authors, modify the configuration file `$APP_DIR/pyrustic_data/hubstore/promotion.json` as follows:
```bash
{ 
    "developer/app-name": "A short description",
    "developer/another-app-name": "A short description"
}
```

`Hubstore` is built with `Pyrustic framework` and is available on PyPI. As `Hubstore` uses the standard Python `Wheel` package format, it is compatible with many existing projects.

## Demo
[Install](#installation) `Hubstore` in a new Python virtual environment. Open `Hubstore`, accept the default configuration to store data in $HOME, then just type in the search bar `pyrustic/demo` or copy-paste `https://github.com/pyrustic/demo`. You will be asked if you want to install the demo app. Once installed, you can run the app. You can also deliberately crash the demo app: just click the `crash` button. `Hubstore` will intercept the crash and it will offer you to report it.


If you are an old user of Hubstore, please delete/move `$HOME/hubstore-apps` and `$HOME/PyrusticData` before you open the new version of `Hubstore`. Yes this new version isn't compatible with the previous one.

Enjoy the demo !

## Installation
If you have never installed a package from PyPI, you must install the pip tool enabling you to download and install a PyPI package. There are several methods which are described on this [page](https://pip.pypa.io/en/latest/installing/).

### Install for the first time
```bash
$ pip install hubstore
```

I recommend even for the first time to use the next command (upgrade). `Hubstore` needs the latest version of its dependencies.

### Upgrade

```bash
$ pip install hubstore --upgrade --upgrade-strategy eager
```

Note: this project is for early-adopters ! Work in progress...