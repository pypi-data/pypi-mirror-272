# Gradema

The utility you need to easily configure auto-grading.

https://pypi.org/project/gradema/

https://gradema.readthedocs.io

Python 3.10 required.

## Try it out

```shell
poetry install
poetry run python -m example.binaryconvert.autograder
```


## Dependencies for student machines

Since Gradema will be published on Pypi, getting this to work should be as simple as having these things installed,
then letting an installer script do the rest:

* [venv](https://docs.python.org/3/library/venv.html) is installed
* Dependencies for libmagic are installed
  * No action is required unless you are running this on Windows and are not using Git Bash
  * See https://github.com/ahupp/python-magic?tab=readme-ov-file#installation

## Project Structure

* `gradema`
  * Contains all the code for gradema
* `example`
  * Contains example usages of gradema
* `tests` (not yet created)
  * Contains unittests to test the functionality of gradema.
  * This is the only place unit tests exist for the project itself. A "unit test" in another location is likely just an example unit test that does not test the functionality of gradema itself

## [Development](./DEVELOPMENT.md)

## Goals

* This should be a thin wrapper around shell commands which actually run tests. This allows people to debug the smaller components themselves. The autograder should be a tool to help people understand these components, rather than a black box.
  * We need to be able to run `pudb -m ...` and have it launch right into the user's code

## Running Tests

All tests are located in the `tests` directory, so you must explicitly state that directory, otherwise some tests will be incorrectly picked up in other directories.

```shell
poetry run pytest tests
```


# TODO

* Use [py2cfg](https://pypi.org/project/py2cfg/) to produce control flow graphs
* Text diff (not critical)
* Do C++ example - lowest priority
* Fuzzy diff support
