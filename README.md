# yt-dlp-api

# Introduction

The simple yt-dlp-api server is for extracting YouTube video information with YouTube video URL.

# Usage

- Preparing the Linux-like operating system.
- Preparing the `Python 3.7+` version in the operating system.
- Install the `pipenv` with running the `pip3 install -U pipenv` command.
- Running the `pipenv install` to create the virtual environment.
- Modifying the `yt-dlp-api.service` file with the `yt-dlp-api.service.example` file.
- Copying the `yt-dlp-api.service` file to the `/etc/systemd/system/` folder.
- Running the `sudo systemctl daemon-reload` to reload the systemd daemon.
- Running the `sudo systemctl enable --now yt-dlp-api.service` to enable and start the service.
- Enjoy it!
