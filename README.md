# mcmapimg
A command-line utility, web application, and Python library to convert Minecraft in-game maps to image files.

## Contents
1. [Dependencies](#dependencies)
2. [Installation](#installation)
3. [Usage](#usage)

## Dependencies

### Required
* [Python](http://python.org) 2.7
* [Python Imaging Library](https://pypi.python.org/pypi/PIL)
* [PyNBT](//github.com/TkTech/PyNBT) (included as a Git submodule)

### Optional
* A [CGI](https://www.w3.org/CGI/)-capable web server (to run the web interface)
* [Git](https://git-scm.com/) (to install from GitHub)

## Installation
1.  Clone this repository into an empty directory:
    ```
    git clone https://github.com/joodicator/mcmapimg
    cd mcmapimg
    ```

2.  Initialise the submodules:
    ```
    git submodule init
    git submodule update
    ```

## Usage
There are three ways to use this tool:

1.  Run `mcmapimg.py` as a command-line program. See the output of:
    ```
    ./mcmapimg.py --help
    ```

2.  Using the web interface: make accessible by a web server `index.htm` and `map.png` - the latter of which is an executable Python script and should be run as a CGI program by the web server - for example, under `http://localhost/mcmapimg`; then navigate to this URL and follow the instructions there.

3.  As a library directly from Python:
    ```
    python2.7
    import mcmapimg
    help(mcmapimg)
    ```
