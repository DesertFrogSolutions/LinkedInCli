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

You will need to add your LinkedIn Username and Password to
`.settings.toml` - see [`settings.example.toml`](./settings.example.toml) for
a template to copy into the correct location.

After installing the dependencies and adding the necessary configuration, run
the application to see usage information with

```sh
pipenv run main
```
or, to be explicit,
```sh
pipenv run python src/main.py
```

The `main` script is defined in the [Pipfile](./Pipfile) to make it easier to
interact with the script. See the defined scripts with the command `pipenv scripts`

To run multiple commands in a row, it may be easier to interact with this script 
in a shell session with the associated Virtualenv activated - to start one, run

```sh
pipenv shell
```

In this shell, commands like `python src/main.py` can be run without reference
to `pipenv`.

## Development Processes

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
We also considered: [Confuse](https://confuse.readthedocs.io/en/latest/usage.html):
there's quite a bit of overlap in the feature sets between Confuse and Dynaconf (and Click)
