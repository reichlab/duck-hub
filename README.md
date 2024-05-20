# Bucket Hub

Experimenal project to explore the possibilites of cloud-based Hubverse data.

## Project setup

### Pre-requisites

- Python 3.12+
- [uv](https://pypi.org/project/uv/): to quickly resolve dependencies and install them into the project's virtual environment (quickest way to get started with uv: `pip install uv`)

### Setup

1. Clone this repo and `cd bucket-hub`
2. Create a virtual environment for the project:
    ```bash
    uv venv
    ```
3. Activate the virtual environment:

    On MacOS and Linux:
   ```bash
   source .venv/bin/activate
   ```

   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

4. Install the project requirements:
    ```bash
    uv pip install -r requirements/requirements.txt && uv pip install -e .
    ```
    Alternately, if you're planning to write code for the project:
    ```bash
    uv pip install -r requirements/requirements-dev.txt && uv pip install -e .
    ```

5. Run the test suite:
    ```bash
    pytest
    ```
