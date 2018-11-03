# BAS Style Kit File Upload Endpoint

A minimal API implementing a simple form action for testing file upload components in the BAS Style Kit.

This API is also used for testing generic features used across BAS APIs. See the [General features](#general-features)
section for more information.

## Purpose

The [BAS Style Kit](https://style-kit.web.bas.ac.uk) includes interactive components for file uploads, to help develop 
these components, and to simulate various error states, a real service which will accept (or decline) uploads was 
needed to give realistic results.

This API provides a set of endpoints which can be used as form actions to test different situations including 
single/multiple uploads and errors such as uploads that are too large. This API is intentionally separate to the Style 
Kit to test cross origin requests, which are restricted by Web Browsers for security.

**Note:** This API is not intended, and does not, store uploaded files. It is not intended for any use beyond testing 
or demonstrating file upload components in the Style Kit.

### Generic features

In addition to providing a file upload endpoint, this API is used for developing features that are common or generic in
nature for use by other BAS APIs. Some of these features are generic, or can demonstrate generic features, such as using
[Request IDs][#request-ids]. Others are features specific to developing APIs using Flask or it's wider ecosystem.

This API is used rather than developing a synthetic 'demonstrator' application and means that effort is not wasted on
an API that does nothing useful by itself. Consequently this API may seem 'over the top' for what it does, which is 
after all, quite simple. Some features, such as database support, are out of scope however, as it wouldn't make sense to 
add based on what this API does.

## Usage

See the [Usage information](/docs/usage.md) for the various endpoints available and general information about this API.

## Implementation

This API is implemented as a minimal Python Flask application. No information is persisted by this API, however logs
may be captured depending on how the API is deployed or for [Error tracking](#error-tracking).

### Configuration

Application configuration is set within `config.py`. Options use global or per-environment defaults which can be 
overridden if needed using environment variables, or a `.env` file (Dot ENV) file. 

Options include values such as application secrets and feature flags, used to enable to disable features such as error
logging.

The application environment is set using the `FLASK_ENV` environment variable. A sample Dot ENV file, `.env.example`, 
describes how to set any required, or frequently changed options. See `config.py` for all available options.

### Request IDs

To aid in debugging, all requests will include a `X-Request-ID` header with one or more values. This can be used to
trace requests through different services such as a load balancer, cache and other layers. Request IDs are managed by 
the *Request ID* middleware. The `X-Request-ID` header is returned to users and other components as a response header.

See the [Correlation ID](https://gitlab.data.bas.ac.uk/WSF/api-load-balancer#correlation-id) documentation for how the
BAS API Load Balancer handles Request IDs.

If there isn't a `X-Request-ID` header, one will be added by this API.

To access the Request ID within the application:

```python
from flask import request

print(request.environ.get("HTTP_X_REQUEST_ID"))
```

### Error tracking

To ensure the reliability of this API, errors are logged to 
[Sentry](https://sentry.io/antarctica/bsk-file-upload-endpoint/) for investigation and analysis.

Through [Continuous Deployment](#continuous-deployment), each commit to the `master` branch in the project repository 
creates a new Sentry release, associated the *production* environment through a deployment using the Sentry CLI.

### Health checks

Endpoints are available to allow the health of this API to be monitored. This can be used by load balancers to avoid
unhealthy instances or monitoring reporting tools to prompt repairs by operators.

#### [GET|OPTIONS] `/meta/health/canary`

Reports on the overall health of this service as a boolean *healthy/unhealthy* status.

Returns a `204 - NO CONTENT` response when healthy. Any other response should be considered unhealthy.

## Setup

### Local development

To setup a local copy of this API access to this repository, Docker and Docker Compose are required. 

```shell
$ cd bas-style-kit-file-upload-endpoint
```

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk), you can pull the application Docker 
image from the BAS Docker Registry. Otherwise you will need to build the Docker image locally.

```shell
# If you have access to gitlab.data.bas.ac.uk
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose pull
# If you don't have access
$ docker-compose build
```

Copy `.env.example` to `.env` and edit the file to set at least any required (uncommented) options.

To run the API using the Flask development server (which reloads automatically if source files are changed):

```shell
$ docker-compose up
```

To run commands against the Flask application (such as [Integration tests](#integration-tests)):

```shell
$ docker-compose run app flask [command]
# E.g.
$ docker-compose run app flask test
```

### Heroku

To setup the Heroku project for this application, access to this repository, Heroku and Terraform is required.

**Note:** Make sure the `HEROKU_API_KEY` and `HEROKU_EMAIL` environment variables are set within your local shell.

```shell
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
[Flasky](https://github.com/miguelgrinberg/flasky) example project [1].

Environments and feature flags are used to control which elements of this application are enabled in different 
situations. For example in the development environment, Sentry error tracking is disabled and Flask's debug mode is on.

New features should be implemented with appropriate [Configuration](#configuration) options available. Sensible defaults 
for each environment, and if needed feature flags, should allow end-users to fine tune which features are enabled.

Ensure `.env.example` is kept up-to-date if any configuration options are added or changed.

Ensure [Integration tests](#integration-tests) are written for any new feature, or changes to existing features.

Ensure the [end user usage](#usage) documentation is kept up-to-date as API methods, options, etc. change.  

[1] If in BAS, access to the associated book is available from the Web & Applications Team.

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Flake8](http://flake8.pycqa.org/) is used to ensure compliance, and is ran on each commit through 
[Continuous Integration](#continuous-integration).

To check compliance locally:

```shell
$ docker-compose run app flake8 . --ignore=E501
```

### Dependencies

Python dependencies should be defined using Pip through the `requirements.txt` file. The Docker image is configured to
install these dependencies into the application image for consistency across different environments. Dependencies should
be periodically reviewed and update as new versions are released.

To add a new dependency:

```shell
$ docker-compose run app ash
$ pip install [dependency]==
# this will display a list of available versions, add the latest to `requirements.txt`
$ exit
$ docker-compose down
$ docker-compose build
```

If you have access to the BAS GitLab instance, push the Docker image to the BAS Docker Registry:

```shell
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose push
```

### Dependency vulnerability scanning

To ensure the security of this API, all dependencies are checked against 
[Snyk](https://app.snyk.io/org/antarctica/project/9e602274-9d5e-4672-8d39-97e6f7657843/history) for vulnerabilities. 

**Warning:** Snyk relies on known vulnerabilities and can't check for issues that are not in it's database. As with all 
security tools, Snyk is an aid for spotting common mistakes, not a guarantee of secure code.

Some vunerabilities have been ignored in this project, see `.snyk` for definitions and the 
[Dependency exceptions](#dependency-vulnerability-exceptions) section for more information.

Through [Continuous Integration](#continuous-integration), on each commit current dependencies are tested and a snapshot
uploaded to Snyk. This snapshot is then monitored for vulnerabilities.

#### Dependency vulnerability exceptions

This project contains known vulnerabilities that have been ignored for a specific reason.

* [Py-Yaml `yaml.load()` function allows Arbitrary Code Execution](https://snyk.io/vuln/SNYK-PYTHON-PYYAML-42159)
    * currently no known or planned resolution
    * indirect dependency, required through the `bandit` package
    * severity is rated *high*
    * risk judged to be *low* given the nature of this API
    * ignored for 1 year for re-review

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit) for issues 
such as not sanitising user inputs or using weak cryptography. 

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the 
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Through [Continuous Integration](#continuous-integration), each commit is tested.

### Logging

In a request context, the default Flask log will include the URL and [Request ID](#request-ids) of the current request.
In other cases, these fields are substituted with `NA`.

**Note:** When not running in Flask Debug mode, only messages with a severity of warning of higher will be logged.

### Reserved routes

These routes are reserved and **MUST NOT** be implemented:

* `/meta/errors/generic-not-found` - used to test the behaviour of a genuine 'not found' URL

### Internal request methods

Some additional API endpoints are available for development/testing purposes. These endpoints are not documented 
publicly and should not be relied upon outside of development or testing.

#### [GET] `/meta/errors/generic-bad-request`

Triggers a generic `400 - Bad Request` error to test the configured error handler. Returns a JSON formatted error.

#### [GET] `/meta/errors/generic-internal-server-error`

Triggers a generic `500 - Internal Server Error` error to test the configured error handler. Returns a JSON formatted
error.

## Testing

### Integration tests

This project uses integration tests to ensure features work as expected and to guard against regressions and 
vulnerabilities.

The inbuilt Python [UnitTest](https://docs.python.org/3/library/unittest.html) library is used for running tests using 
Flask's test framework. Test cases are defined in files within `tests/` and are automatically loaded when using the 
`test` custom Flask CLI command.

To run tests manually:

```shell
$ docker-compose run -e FLASK_ENV=testing app flask test
```

Pip dependencies are [checked](#dependency-vulnerability-scanning) on each commit and then monitored for future
vulnerabilities.

Tests are automatically ran on each commit through [Continuous Integration](#continuous-integration).

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

This process will run the application [Integration tests](#integration-tests).

### Review apps

To allow unreleased changes to be viewed by others, short-term instances of this API (known as review apps) are created 
on each commit within a branch, except the *master* branch, which is part of [Deployment](#deployment)). Review apps 
are managed by GitLab as part of [Continuous Integration](#continuous-integration).

Each review app is a standalone Heroku application, configured in the same way as the production instance. The URL for
each application is computed based on a common prefix (`bas-ra`), the project (in GitLab) and CI/CD pipeline being ran. 
See the [Herok](#heroku) section for more information on how this project runs on Heroku.

## Deployment

### Heroku

This API is deployed on [Heroku](https://heroku.com) as a 
[app](https://dashboard.heroku.com/apps/bas-style-kit-file-upload) under the `webapps@bas.ac.uk` shared account, 
using their [container hosting](https://devcenter.heroku.com/articles/container-registry-and-runtime) option.

The Heroku project uses a Docker image built from the application image with the application source included and 
development related features disabled. This image is built and pushed to Heroku on each commit to the `master` branch 
through [Continuous Deployment](#continuous-deployment).

**Note:** This deployment is considered both a *staging* and *production* environment due to the low value and developer
oriented nature of this API. The *development* environment is not deployed as it is only intended for local use.

### Continuous Deployment

All commits to the `master` branch will trigger a Continuous Deployment process using GitLab's CI/CD platform, 
configured in `.gitlab-ci.yml`.

This process will build a Heroku specific Docker image using a 'Docker In Docker' (DIND/DND) runner and push this image
to Heroku.

It will also create a Sentry release and associated deployment of the release to a *production* environment.

## Release procedure

### At release

1. create a release branch
2. remove `-develop` from version string in:
  * `docker-compose.yml` - app Docker image
  * `.gitlab-ci.yml` - default Docker image
  * `Dockerfile.heroku` - `FROM` directive
3. build & push the Docker image
4. close release in `CHANGELOG.md`
5. push changes, merge the release branch into `master` and tag with version
6. delete the `-develop` tag from the project container registry

The application will be automatically deployed into production using [Continuous Deployment](#continuous-deployment).

### After release

1. create a next-release branch
2. bump the version with `-develop` appended in:
  * `docker-compose.yml` - app Docker image
  * `.gitlab-ci.yml` - default Docker image
  * `Dockerfile.heroku` - `FROM` directive
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
