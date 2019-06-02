![Colour My Change Logo](/src/static/img/box_logo.png)

# Colour My Change
A web application for generating a weight change and fitness roadmap.

## Project Architecture
* kubernetes (manifests for deployment)
    * Manifests for deployment
* src (source files for the app)
    * backend (generation logic for the PDFs)
    * static (static files to serve, like logos)
    * templates (HTML templates)


## Installing Dev Environment
To install a development environment, first make sure you have the following requirements.

```
docker
```

Next, clone the repo, cd into it, and run the `make install` command. This will build and tag the docker image with variables in the Makefile.

Once built, use the `make run` command to run a local version on your machine - no kubernetes is required, as it's just a simple docker container.

## Deployment
To push to gcr.io, increment version in the Makefile and run the `make push` command. When ready, increment the version in kubernetes/deployment.yaml and run the `make deploy` command to roll out the changes to the cluster.
