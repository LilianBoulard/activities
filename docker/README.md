# Deploying with Docker

As mentioned in the project's README, the simplest way of running the project 
is by using docker.

We will see here how to deploy it.

## Use locally

The first and simplest step is to create the containers by running

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
