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

# Tips

- Sometimes the `yt-dlp` are updated frequently and it can run the `pipenv run pip install -U yt-dlp` command to upgrade this package and run the `systemctl restart yt-dlp-api.service` command to restart the daemon service.
- Since the yt-dlp `2024.11.04` version has been released, the minimal Python version is `3.9` and the `yt-dlp-api` will support Python `3.9` at least becasue of compatibility.
