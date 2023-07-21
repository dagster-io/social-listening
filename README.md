# Social Listening

This is a [Dagster](https://dagster.io/) project scaffolded with [`dagster project scaffold`](https://docs.dagster.io/getting-started/create-new-project). It listens to all the mentions of a given keyword in various social platforms and send each mention as individual Slack message to a channel to build an aggregated social feed.


| High-level  | Dagster UI |
| ------------- | ------------- |
| ![diagram](https://github.com/dagster-io/social-listening/assets/4531914/ecd8a96c-33bd-431a-9560-80a2c0047b02) | ![ui](https://github.com/dagster-io/social-listening/assets/4531914/9b480a88-fef8-4b70-be1a-d98535a11deb) |

## Getting started

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `social_listening/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.


### Using environment variables to handle secrets

Dagster allows using environment variables to handle sensitive information. You can define various configuration options and access environment variables through them. This also allows you to parameterize your pipeline without modifying code. Check out Using environment variables and secrets guide for more info and examples.

To successfully load this project, you'll need the following environment variables set:
```
REDDIT_PERSONAL_USE_SCRIPT
REDDIT_SECRET
REDDIT_USERNAME
REDDIT_PASSWORD
SLACK_BOT_TOKEN
```

You can declare environment variables in various ways:
- **Local development**: [Using `.env` files to load env vars into local environments](https://docs.dagster.io/guides/dagster/using-environment-variables-and-secrets#declaring-environment-variables)
- **Dagster Cloud**: [Using the Dagster Cloud UI](https://docs.dagster.io/master/dagster-cloud/developing-testing/environment-variables-and-secrets#using-the-dagster-cloud-ui) to manage environment variables
- **Dagster Open Source**: How environment variables are set for Dagster projects deployed on your infrastructure depends on where Dagster is deployed. Read about how to declare environment variables [here](https://docs.dagster.io/master/guides/dagster/using-environment-variables-and-secrets#declaring-environment-variables).

Check out [Using environment variables and secrets guide](https://docs.dagster.io/guides/dagster/using-environment-variables-and-secrets) for more info and examples.


## Code Structure
To understand the structure, start with the file `social_listening/__init__.py`. This project includes a few key Dagster concepts:

- **Assets**: assets are used to represent the data of social mentions.
- **Sensors** are used to run jobs or assets based on external events, see `social_listening/sensors/`.
- **Resources**: are primarily used to represent external systems. For example, this project uses resources for connecting to Slack. The project also shows how to create custom resources, see `social_listening/resources.py`.


## Development


### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Unit testing

Tests are in the `social_listening_tests` directory and you can run tests using `pytest`:

```bash
pytest social_listening_tests
```

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.

## Deploy on Dagster Cloud

The easiest way to deploy your Dagster project is to use Dagster Cloud.

Check out the [Dagster Cloud Documentation](https://docs.dagster.cloud) to learn more.
