# yt-dlp-api

# Introduction

1. The simple yt-dlp-api server is for extracting YouTube video information with YouTube video URL.
2. We provide the simple web UI for accessing, using and downloading YouTube video easily.
3. It can use the `docker` to build and run this server easily.

# Prerequisite

- The `docker` command is available.

# Usage

- Since YouTube JS challenge mechanism is changed, we only support the `0.2.0+` version currently because the old version is deprecated.

- Preparing the Linux-like operating system.
- Installing the `docker`.
- Running the `docker compose build` to build this Docker compose.
- Running the `docker compose up -d` to run this server as the background service.
- Using the prefered web browser to browse the `http://localhost/web/index_en.html`.
- Enjoy it!

# Tips

- If you want to change the Nginx port number, please edit the [nginx.ports](https://github.com/peter279k/yt-dlp-api/blob/master/docker-compose.yml#L60) setting.
