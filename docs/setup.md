## Setup

### Local

Create `.env` based on `.env.example`, items prefixed with `#` are optional, others MUST be set.

### Heroku

Run Terraform to create application.

Set sensitive environment/config variables in Heroku dashboard:

| Config Var   | Config Value            | Description                                                 |
| ------------ | ----------------------- | ----------------------------------------------------------- |
| `SENTRY_DSN` | *Available from Sentry* | Identifier for application in Sentry error tracking service |
