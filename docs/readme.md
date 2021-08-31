# Getting Started

This project requires a running instance of [Mastodon](https://github.com/mastodon/mastodon), a federated open source social media platform.  


Mastodon developers offer a solid  `docker-compose` option  for ready to go configuration.

Therefore a cloud instance is required ex. Google Cloud, Amazon Web Services, Linode, DigitalOcean

We recommend an Ubuntu 20.04 LTS machine with 2 GB of RAM and min 20 GB of disk space.

```{note} 
A domain name is also required for production. It can be acquired with `GitHub Student Developer Pack`. [See further](https://education.github.com/pack)  
`.tech` domains are recommended. 
```



## Install Docker
Second step is to install `Docker Engine` on Ubuntu.

### Set up the repository
1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:

        sudo apt-get update

        sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
2. Add Docker’s official GPG key:

        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
3. Use the following command to set up the stable repository.

        echo \
        "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
### Install Docker Engine
1. Update the apt package index, and install the latest version of Docker Engine and containerd

        sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io
2. Verify that Docker Engine is installed correctly by running the hello-world image

        sudo docker run hello-world





### Install Docker Compose

#### Install Compose on Linux systems
1. Run this command to download the current stable release of Docker Compose:

        sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
2. Apply executable permissions to the binary

        sudo chmod +x /usr/local/bin/docker-compose
3. Test the installation.

        docker-compose --version

If any problems with these steps read further:
[Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)  

[Install Docker Compose](https://docs.docker.com/compose/install/)


### Manage Docker as a non-root user

To create the `docker` group and add your user:

1. Create the `docker` group.

        sudo groupadd docker

2. Add your user to the `docker` group.

        sudo usermod -aG docker $USER

3. Log out and log back in so that your group membership is re-evaluated.

    If testing on a virtual machine, it may be necessary to restart the virtual machine for changes to take effect.

    On Linux, you can also run the following command to activate the changes to groups:

        newgrp docker

4. Verify that you can run `docker` commands without `sudo`

        docker run hello-world


# Mastodon Docker Setup

## Setting up

Launch a console terminal on the remote machine.

Clone Mastodon's repository.
    
    # Clone mastodon to ~/mastodon directory
    git clone https://github.com/mastodon/mastodon.git mastodon
    # Change directory to ~/mastodon
    cd ~/mastodon
    # Checkout to the latest stable branch
    git checkout $(git tag -l | grep -v 'rc[0-9]*$' | sort -V | tail -n 1)
    


## Installing Docker containers

```{admonition} Docker Images
:class: tip

You can use a prebuilt Docker image. Images are available from Docker Hub:  
[Mastodon Docker Image](https://hub.docker.com/r/tootsuite/mastodon/)
```

## Docker Compose and and environment files
Use these pre-configured files to avoid any problems.
[Github](https://github.com/dogukanburda/mastodon-dockerized-production)

## Building the app

Copy the files `.env.production` and  `.env.db` that have been provided to the `/mastodon` directory.
Then change the `docker-compose.yml`  file with provided one.

In `env.production` file replace  `LOCAL_DOMAIN`  with your own domain name.

To create an account for admin run the followings: 

    docker-compose run --rm web bundle exec rake mastodon:setup


This is an interactive wizard that will guide you through the basic and necessary options and generate new app secrets. 

App secrets part did not worked for me before so we generated them beforehand.
  1. Enter the Fully Qualified Domain Name (FQDN) of your mastodon instance.
  2. Select if you want a Single User instance (not recommended, but if you prefer, use that).
  3. Obviously, you are running mastodon in a docker instance, so type Y (or hit return, as it's the default)
  4. The PostgreSQL host is `db`, the port is `5432` (again, default), the database is `mastodon_production`, the database user is `mastodon` and the password is the one from `docker-compose.yml`.
  5. The redis server is `redis`, the port is `6379` and the password is empty. 
  6. If you want to store uploaded files on the cloud, enter Y here – I haven't tested that, but I expect you need an S3 or other cloud storage for that.
  7. If you want to send emails from the local machine, enter `Y` – considering we're in a docker environment, I have only used my local STMP server in FQDN form, not `localhost`. Enter port, user and password for SMTP `submission`. Select the SMTP authentication type (when submitting locally, `plain` should be fine). Decide if you want to verify the identity of the server and, if so, what type of verification you want to do. Choose what sender address the emails will have (I use `mastodon@*my.domain*`). 

#### DNS Configuration

Add `A Record` to instance IP with your DNS manager.

### Reverse Proxy
You need a Reverse Proxy in front of your Mastodon instance. The preferred software for this Caddy 2 which is already a part of `docker-compose.yml` file that provided.  

Caddy 2 is still the only web server to use TLS automatically and by default. Caddy 2 
enables to deploy and scale HTTPS effortlessly.


#### Caddyfile Configuration



You need to configure [Caddy](https://caddyserver.com/v2) to serve your [Mastodon](https://github.com/tootsuite/mastodon/) instance.

**Reminder: Replace all occurrences of example.com with your own instance's domain or sub-domain.**

Create a `Caddyfile` containing only these lines and replace `your.domain.tech` with your own domain:  

        your.domain.tech {
        reverse_proxy web:3000
        }




## Launch Mastodon
After it's done, you can launch Mastodon with:

    docker-compose up -d
    
Within ~30 seconds all docker containers should be up and running.
You can check it with `docker ps` command.

## Creating accounts
Main admin account is created when building the app. Any other accounts must be created and confirmed on the terminal with admin CLI that Mastodon provides.
Since an e-mail delivery service or other SMTP server is not dedicated for the server, its only possible to confirm users with the admin CLI tool.

Execute the following command on the terminal where the `docker-compose.yml` file exists to create an account 

        docker-compose run --rm web bin/tootctl accounts create USERNAME --email EMAIL --confirmed

Replace `USERNAME` and `EMAIL` with relevant information.

If an account is created at sign-up page and waiting for confirmation, user can be modified with the following command:

        docker-compose run --rm web bin/tootctl accounts modify USERNAME --confirm


For further information about admin CLI, you can check out [Using the admin CLI](https://docs.joinmastodon.org/admin/tootctl/) 

----------

```{include} ./readme2.md
```



## Resources

* [https://github.com/tootsuite/documentation/blob/master/Running-Mastodon/Docker-Guide.md](https://github.com/tootsuite/documentation/blob/master/Running-Mastodon/Docker-Guide.md)
* [https://github.com/tootsuite/documentation/blob/master/Running-Mastodon/Production-guide.md](https://github.com/tootsuite/documentation/blob/master/Running-Mastodon/Production-guide.md)
