# LinkedIn Data Takeout

This script scrapes data from a user's [LinkedIn](https://www.linkedin.com/).

## Getting Started

You will need [Pipenv](https://pipenv.pypa.io/en/latest/) to install
dependencies for this project, and a recent version of Python 3.x.

To install the production dependencies, just run
```sh
pipenv sync
```

### Configure & Run The App

You will need to provide the LinkedIn Username and Password on the command line or add them to `.secrets.toml` - see [`secrets.example.toml`](./secrets.example.toml) for a template to copy into the correct location.

After installing the dependencies and adding the necessary configuration, run
the application to see usage information with

```sh
pipenv run main
```
or, to be explicit,
```sh
pipenv run python src/main.py
```

The `main` shortcut is defined in the [Pipfile](./Pipfile) to make it easier to
interact with the application. See the defined shortcuts with the command `pipenv scripts`

To run multiple commands in a row, it may be easier to interact with this application
in a shell session with the associated Virtualenv activated - to start one, run

```sh
pipenv shell
```

In this shell, commands like `python src/main.py` can be run without reference
to `pipenv`.

## Development Processes

[Pipenv](https://pipenv.pypa.io/en/latest/) is an application that makes it easy to work with application dependencies and [virtual environments](https://docs.python.org/3/library/venv.html). Isolating dependencies for different applications from each other using a virtual environment is a common practice that pipenv implements along with many other Python ecosystem best practices. See [e.g.](https://towardsdatascience.com/a-guide-to-python-good-practices-90598529da35) for more information about virtual environments.

Starting a new project with `pipenv` is easy - just run

```sh
pipenv --three
```

to create a new virtualenv with Python 3 for your project.

To install the dependencies needed to develop the project, run

```sh
pipenv install --dev
```

Install a new package, for instance, `dynaconf`, with

```sh
pipenv install dynaconf
```

After adding the packages you need, generate a new `Pipfile.lock` with

```sh
pipenv lock
```

### Implementation Choices

As this application interfaces with LinkedIn through the [linkedin-api](https://github.com/tomquirk/linkedin-api),
we require a valid LinkedIn username and password.
We manage configuration using the [dynaconf](https://github.com/rochacbruno/dynaconf) package.
supports securely managing configuration parameters.
The CLI is built with [Click](https://click.palletsprojects.com/en/8.0.x/),
which is used for the CLI in the Flask project.

## Roadmap

- v1.0
  - [Tests](https://click.palletsprojects.com/en/8.0.x/testing/) for common CLI actions with [pytest](https://docs.pytest.org/en/7.0.x/)
  - Parsed/friendly output for activity feed
  - Improved support for linkedin_api interface
