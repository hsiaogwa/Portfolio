# Quart Web Service for Alven.space
## Introduction
## 1. How to build up
> **You can use our bash-to-setup**
> ```bash
> ubuntu@alven.space:*/WebService/bin $ sudo chmod +x active.sh
> ubuntu@alven.space:*/WebService/bin $ ./active.sh
> ```
Whatelse, you can only use docker to test on local host.
[Local Docker](#docker-id)
### 1.1 Ensure your Nginx
```bash
ubuntu@alven.space:*/WebService $ cp bin/nginx/nginx.conf /etc/nginx/nginx.conf
ubuntu@alven.space:*/WebService $ cp bin/nginx/sites-available/alven.space.conf /etc/nginx/sites-available/alven.space.conf
ubuntu@alven.space:*/WebService $ sudo ln -s /etc/nginx/sites-available/alven.space.conf /etc/nginx/sites-enabled/alven.space.conf
ubuntu@alven.space:*/WebService $ sudo systemctl reload nginx
```
  <button
    onclick=""
	style="
	/*css*/
	">Copy
  </button>
### 1.2 Install CA
### 1.3 Make Up Docker Container <lable id="docker-id" />
```bash
ubuntu@alven.space:*/WebService $ sudo docker compose up --build -d
```