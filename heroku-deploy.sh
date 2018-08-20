#!/usr/bin/env bash -eux

docker build -t registry.heroku.com/bas-style-kit-file-upload/web -f Dockerfile.heroku .
docker push registry.heroku.com/bas-style-kit-file-upload/web
heroku container:release web --app bas-style-kit-file-upload
