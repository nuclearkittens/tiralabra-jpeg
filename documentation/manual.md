# User manual

The application can be run using the command line. Poetry is used to manage dependencies, and Invoke to run the application as well as several other tasks.

1. Clone the repository: `git clone git@github.com:nuclearkittens/ot-projekti.git`
2. Install dependencies: `poetry install`
3. Run the application: `poetry run invoke start`
    + The application has a terminal interface, and gives you instructions on how to use it
4. Run tests: `poetry run invoke test`
5. Generate a test coverage report: `poetry run invoke coverage-report`
    + Report can be found in `htmlcov` directory
6. Check code quality: `poetry run invoke lint`

Only the example of functionality is currently implemented. It can be run by starting the application, and you have the option to run it with small randomly created images and some bigger actual images. Compressing the bigger images takes quite a while, though (15-ish minutes with my setup), and during that the only(?) way to quit the application is to raise a `KeyboardInterrupt` (ctrl/cmd+c).
