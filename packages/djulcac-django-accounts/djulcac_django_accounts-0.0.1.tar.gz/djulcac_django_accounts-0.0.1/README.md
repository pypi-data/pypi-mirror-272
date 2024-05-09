# DJANGO-ACCOUNTS

## Packaging

Based on this [documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/)


Generating distribution archives

    python3 -m pip install --upgrade build
    python3 -m build

Uploading the distribution archives

    python3 -m pip install --upgrade twine
    python3 -m twine upload dist/*
