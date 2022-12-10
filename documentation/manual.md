# User manual

*needs to be rewritten, this is mostly a placeholder*

Only the example of functionality is currently implemented.

The application can be run using the command line. Poetry is used to manage dependencies, and Invoke to run the application as well as several other tasks.

1. Clone the repository: `git clone git@github.com:nuclearkittens/ot-projekti.git`
2. Install dependencies: `poetry install`
3. Run the application: `poetry run invoke start`
4. Run tests: `poetry run invoke test`
5. Generate a test coverage report: `poetry run invoke coverage-report`
    + Report can be found in `htmlcov` directory
6. Check code quality: `poetry run invoke lint`
