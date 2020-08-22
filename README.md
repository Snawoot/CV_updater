# CV\_updater
Python script to update your CV on https://hh.ru/

## Requirements 

You need to have installed Chromium browser.

## Installation

Run within source directory:

`pip3 install .`

`hh-cv-updater` executable command should become immediately available. Alternatively, you may invoke application with `python3 -m hh_cv_updater ...` command

## Set your account

Run:

```
hh-cv-updater login
```

Browser window will pop up, prompting user to login. Once login will be acknowledged by application, browser window will be closed.

## Update all resumes

Run:

```
hh-cv-updater update
```

Application will be running continously, updating all your CV's in random intervals about to 4 hours. If application is being restarted, it will figure out next update from own records on last update.
