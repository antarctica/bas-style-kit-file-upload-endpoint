# Deployment

To push an application release (Docker image) to Heroku:

**Note:** Ensure you are logged into both the BAS and Heroku Docker registries

```
$ docker-compose build
$ docker-compose push
# Re-tag built image for Heroku
$ docker tag <image> registry.heroku.com/bas-style-kit-file-upload/web
$ docker push registry.heroku.com/bas-style-kit-file-upload/web
$ heroku container:release web --app bas-style-kit-file-upload
```
