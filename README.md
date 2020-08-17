# mcmapimg
A command-line utility, web application, and Python library to convert Minecraft in-game maps to image files.

## Contents
1. [Dependencies](#dependencies)
2. [Installation](#installation)
3. [Usage](#usage)

## Dependencies
### Required
* [Python](http://python.org) 3
* [Python Imaging Library](https://pypi.org/project/PIL/)
* [NBT](https://pypi.org/project/NBT/)

### Optional
* A [CGI](https://www.w3.org/CGI/)-capable web server (to run the web interface)
* [Git](https://git-scm.com) (to install from GitHub)

## Installation
1.  Clone this repository into an empty directory:

    ```
    git clone https://github.com/joodicator/mcmapimg.git
    cd mcmapimg
    ```

## Usage
There are three ways to use this tool:

1.  Run `mcmapimg.py` as a command-line program. See the output of:
    ```
    ./mcmapimg.py --help
    ```

2.  Using the web interface: make accessible by a web server `index.htm` and `cgi-bin/map.cgi` - the latter of which is an executable Python script and should be run as a CGI program by the web server - for example, run python's built-in http server:
    ```
    python -m http.server --cgi 8000
    ```
    Then visit `http://localhost:8000` in your browser and follow the instructions there.

3.  As a library directly from Python:
    ```
    python
    >>> import mcmapimg
    >>> help(mcmapimg)
    ```
