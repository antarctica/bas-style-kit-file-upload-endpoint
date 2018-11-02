# BAS Style Kit File Upload Endpoint - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed [BREAKING!]

* API placed under the BAS API Load Balancer (Test environment), endpoint URLs have changed
* API is now versioned, all existing features are placed in a `v1` version

### Added

* Documented how this API is used more widely for testing generic features and acting as an example Flask API
* Versioning policy
* Deprecation policy
* change log for API rather than project changes, aimed at end-users

### Changed

* Improving end-user usage information

## 0.2.0 (2018-10-31) [BREAKING!]

### Changed [BREAKING]

* Sentry updated to new packages, new DSN required

### Added

* Canary health check endpoint
* Request ID support
* Additional tests to check underlying Flask application exists and correct configuration used
* Heroku review applications
* Snyk for checking Python dependency versions
* Automatic PEP-8 checking using Flake8
* Static security testing using Bandit
* Sentry environment tracking using the existing `FLASK_ENV` environment variable
* Sentry release tracking using a build argument in the Heroku Docker image set in CD
* Sentry release deployment using the Sentry CLI as a job in CD
* GitLab environment information for Heroku as a production environment
* Documenting index request standalone methods in usage documentation
* Documenting content-types, encoding and endpoints/access, error logging and support in usage documentation

### Fixed

* Removing superfluous RUN statement in Dockerfile to create working directory
* Added missing HTTP method/verbs to standalone methods in usage documentation
* Environment variables for boolean options are now correctly cast to the boolean data type
* PEP-8 style violations

### Changed

* Heroku application is now registered under the shared `webapps@bas.ac.uk` account
* Terraform updated to version 0.11.8
* Meta routes and generic errors refactored into a new 'meta' blueprint
* Tests for new meta blueprint moved into a separate test class
* Passing pre-formed keyword argument dicts from the Config class for Flask 'plugins'
* Ensuring the correct Flask/App environment is used when testing
* Improving README

## 0.1.0 (2018-08-28)

### Added

* Creating new project
