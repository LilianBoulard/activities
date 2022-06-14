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

## Open the service the Internet

To open it on the internet, you'll have to:
- Open the appropriate ports on your box
- Use `nginx` for its reverse-proxy / load-balancing / SSL certs. capabilities
  - There are alternatives, like [`swag`](https://docs.linuxserver.io/general/swag)

See [this nice blog post](https://www.javacodemonk.com/part-2-deploy-flask-api-in-production-using-wsgi-gunicorn-with-nginx-reverse-proxy-4cbeffdb#_nginx_setup_configuration)
for more information on this process.
