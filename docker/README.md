Docker is cool, so we use it 😎

* Okay, but *why* ?

🙄 well... actually, there's a few reasons -

## Separation of concerns

Each service has its own individual utility, and they do just that.

## Security

They are all separated from each other, and most importantly from the host.  
This means that even if our app where to be hacked into, we'd still be pretty much safe !

## Scalability

Not enough Redis resources ? Just fire another container.  
Not enough MariaDB resources ? Just fire another container.  
Not enough server resources ? Yes, firing another container is all you need to do 🥵

## Shareability 

You want to run this service on your own computer, and tweaking your settings are not an option ?

That's great : **our dockerfile is all you need** 🤯 !

# Deploying with Docker

Now that we've seen why Docker is great and some of the reasons we use it, 
let's actually put in practice the last point we mentioned !

## Prerequisites

- Install docker and docker-compose
  - If your OS is debian-based, that'll look like this:
    ```commandline
    sudo apt-get install docker docker-compose
    ```
- Install `python3` and `git` (they are installed by default on most linux distributions)

## Use locally

The first and simplest step is to create new passwords for the database:

```commandline
python docker/generate_passwords.py
```

the containers by running

```commandline
sudo docker-compose up -d
```

in the parent folder.

At this point, the project is ready for a local usage.

## Notes on usage and code versioning

To use the code you're modifying directly (so, for development purposes), 
use the `server_dev`'s port otherwise, to use the code from the GitHub repository, 
use the `server`'s port.

To keep your instance always up to date compared to the GitHub repository,
you can set up a git-based stack on portainer.
See [this blog post](https://tobiasfenster.io/use-portainer-to-deploy-and-update-docker-container-stacks-from-a-git-repo).

## Open the service on the Internet

To open your instance on the Internet, you'll have to:
- Open the appropriate port(s) on your box
- Use `nginx` for its reverse-proxy / load-balancing / SSL certs. capabilities
  - There are alternatives, like [`swag`](https://docs.linuxserver.io/general/swag)
  - See [this nice blog post](https://www.javacodemonk.com/part-2-deploy-flask-api-in-production-using-wsgi-gunicorn-with-nginx-reverse-proxy-4cbeffdb#_nginx_setup_configuration)
  for more information on this process.
