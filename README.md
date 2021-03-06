# Rag
*Make creating rest APIs in Django simple.*

Rag is a simple batteries included tool to make building rest API's using Django fast and easy.

## Usage

#### Quick Start

#### Command Line
The command line interface has commands to start a dev server, run development shell, run tests, run Django management commands, create an empty example project, and run a Celery background task worker.

#### Validation
  To validate a field you must start with a root validator: `to`, `am`, `accepts`, or `optional`.  All root
  validators check that a field is defined before proceeding with the exception of `optional` which will
  immediately accept if the field is undefined on the json object.

## Contributing

#### Lauching Dev Stack
Use docker compose to launch development stack.

#### Dev Setup
To install development requirements.
`poetry install`

#### Running Dev Tests
To run tests:  
`poetry run pytest`

To run a specific test suite:  
`poetry run pytest -s -k test_rag`

To run a specific test in a suite:  
`poetry run pytest -s -k "test_validate and test_check"`

To run tests with auto reload:  
`poetry env PYTHONPATH="/rag/tests" ptw`

To run tests with auto reload and specific test:  
`poetry env PYTHONPATH="/rag/tests" ptw --runner "pytest -s -k test_rag"`

To see print statements of passing tests use the `-s` flag

Note: Errors like this might have a root exception with more detail and may mean you are missing migrations:
`psycopg2.errors.InvalidCursorName`
