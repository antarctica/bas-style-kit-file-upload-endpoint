# BAS Style Kit File Upload Endpoint

A minimal API implementing a simple form action for testing file upload components in the BAS Style Kit.

**Note:** This API is not included in [api.bas.ac.uk](https://api.bas.ac.uk).

## Purpose

The [BAS Style Kit](https://style-kit.web.bas.ac.uk) includes interactive components for file uploads. To develop these
components, and to simulate various error states, a real service which will accept (or decline) uploads was needed.

This API provides this service in the form of several endpoints configured with different behaviours including single
and multiple uploads and errors such as files that are too large. This API is intentionally separate to the Style Kit
to test cross origin requests, which are restricted by web browsers.

**Note:** This API is not intended, and does not, store uploaded files. It is not intended to have any use beyond
testing or demonstrating the file upload components in the Style Kit.

## Usage

See the [Usage information](/docs/usage.md) for the various endpoints available and general information about this API.

## Implementation

This API is implemented as a minimal Python Flask application. No information is persisted by this API, however logs
may be captured depending on how the API is deployed or for [Error tracking(#error-tracking).

### Configuration

Application configuration is set within `config.py`, with options defined within per-environment defaults or values set
in configurations for each environment (determined using the `FLASK_ENV` environment variable).

Values for most configuration options can be set using environment variables, or a `.env` file (dot ENV) file. A sample
file (`.env.example`) describes how to set the options available and whether any are required.

### Error tracking

To ensure the reliability of this API, server side errors, and unhandled client side errors, are logged to 
[Sentry](https://sentry.io/antarctica/bsk-file-upload-endpoint/) for investigation and analysis.

## Setup

### Local development

To setup a local copy of this API access to this repository and Docker/Docker Compose is required. 

```
$ cd bas-style-kit-file-upload-endpoint
```

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk) you can pull the application Docker 
image from the BAS Docker Registry. Otherwise you will need to build the Docker image locally.

```
# If you have access to gitlab.data.bas.ac.uk
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose pull
# If you don't have access
$ docker-compose build
```

Copy `.env.example` to `.env` and edit the file to set at least any required (uncommented) options.

To run the API using the Flask development server (where changes to source files will reload the server automatically):

```
$ docker-compose up
```

To run commands against the Flask application (such as integration tests):

```
$ docker-compose run app flask [command]
# E.g.
$ docker-compose run app flask test
```

### Heroku

To setup the Heroku project for this application access to this repository, Heroku and Terraform is required.

**Note:** Make sure the `HEROKU_API_KEY` and `HEROKU_EMAIL` environment variables are set within your local shell.

```
$ cd bas-style-kit-file-upload-endpoint
$ cd provisioning/terraform
$ docker-compose run terraform
$ terraform init
$ terraform apply
```

Visit the [Heroku project settings](https://dashboard.heroku.com/apps/bas-style-kit-file-upload/settings) to set
Config Vars (environment variables) for sensitive settings:

| Config Var   | Config Value            | Description                                         |
| ------------ | ----------------------- | --------------------------------------------------- |
| `SENTRY_DSN` | *Available from Sentry* | Identifier for application in Sentry error tracking |

## Development

This API is developed as a Flask application using the conventions outlined in the 
[Flasky](https://github.com/miguelgrinberg/flasky) example project (if in BAS, access to the associated book is 
available from the Web & Applications Team).

Environments and feature flags are used to control which elements of this application are enabled in different 
situations. For example in the development environment Sentry error tracking is disabled and Flask's debug mode is on.
Ensure appropriate [Configuration](#configuration) options are available for for more information.

New features should be implemented with appropriate [Configuration](#configuration) options available. Sensible defaults 
for each environment, and if needed feature flags, should allow end-users to fine tune which features are enabled.

**Note:** Ensure `.env.example` is kept up-to-date if any configuration options are added or changed.

Ensure integration tests are written for any new feature, or changes to existing features, see [Testing](#testing) for
more information.

### Code Style

The PEP-8 style and formatting recommendations should be used for this project.

### Dependencies

Python dependencies should be defined using Pip through the `requirements.txt` file. The Docker image is configured to
install these dependencies into the application image for consistency across different environments. Dependencies should
be periodically reviewed to update when new versions are released.

To add a new dependency:

```
$ docker-compose run app ash
$ pip install [dependency]==
# this will display a list of available versions, add the latest to `requirements.txt`
$ exit
$ docker-compose down
$ docker-compose build
```

If you have access to the BAS GitLab instance, push the Docker image to the BAS Docker Registry:

```
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose push
```

## Testing

### Integration tests

This project uses integration tests ensure functionality works as expected and to guard against regressions.

The inbuilt Python [UnitTest](https://docs.python.org/3/library/unittest.html) library is used for running tests using 
Flask's test framework. Test cases are defined in files within `tests/` and are automatically loaded and ran when using
the `test` command added to the Flask CLI.

To run existing tests manually:

```
$ docker-compose run app flask test
```

Tests are automatically ran on each commit through [Continuous Integration](#continuous-integration).

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

This process will run the application [Integration tests](#integration-tests).

## Deployment

### Heroku

This API is deployed on [Heroku](https://heroku.com) as a 
[project](https://dashboard.heroku.com/apps/bas-style-kit-file-upload) using their 
[container hosting](https://devcenter.heroku.com/articles/container-registry-and-runtime) option.

The Heroku project uses a Docker image built from the application image with the application source included and 
development related features disabled. This image is built and pushed to Heroku on each commit to the `master` branch 
through [Continuous Deployment](#continuous-deployment).

**Note:** This deployment is considered both a *staging* and *production* environment due to the low value and developer
oriented nature of this API. The *development* environment is not deployed as it is only intended for local use.

**Note:** The Heroku project for this API is currently in a personal account, it will be moved to a team account soon.

### Continuous Deployment

All commits to the `master` branch will trigger a Continuous Deployment process using GitLab's CI/CD platform, 
configured in `.gitlab-ci.yml`.

This process will build a Heroku specific Docker image using a 'Docker In Docker' (DIND/DND) runner and push this image
to Heroku.

## Release procedure

### At release

1. create a release branch
2. remove `-develop` from version string in:
  * `docker-compose.yml` - app Docker image
  * `.gitlab-ci.yml` - default Docker image
3. build & push the Docker image
4. close release in `CHANGELOG.md`
5. push changes, merge the release branch into `master` and tag with version

The application will be automatically deployed into production using [Continuous Deployment](#continuous-deployment).

### After release

1. create a next-release branch
2. bump the version with `-develop` appended in:
  * `docker-compose.yml` - app Docker image
  * `.gitlab-ci.yml` - default Docker image
3. build & push the Docker image
4. push changes and merge the next-release branch into `master`

The application will be automatically deployed into production using [Continuous Deployment](#continuous-deployment).

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at: 
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the 
[Issue tracker](https://gitlab.data.bas.ac.uk/web-apps/bsk/bas-style-kit-file-upload-endpoint/issues) for more 
information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

© UK Research and Innovation (UKRI), 2018, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under 
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at http://www.nationalarchives.gov.uk/doc/open-government-licence/
