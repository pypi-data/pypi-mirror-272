# Install poetry
python -m pip install poetry


# Create a new project with src layout
poetry new --src my_project

# Add dev dependencies
poetry add -D mypy flake8

# Add dependencies
poetry add requests pytest

# remove dependencies
poetry remove requests

# Install dependencies
poetry install

# Show dependencies
poetry show --tree

# Lint the project
poetry run flake8


# test the project
poetry run pytest -s -v

# run the project
poetry run python src/my_package/main.py

# build the project
poetry build


# FAQ
- What is Poetry - dependency management and packaging tool for Python

- poetry.lock should be committed to the repository


