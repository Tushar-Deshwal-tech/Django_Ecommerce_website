# Welcome to our E-commerce Django Project!

This repository contains our exciting e-commerce website built using Django. Get started quickly and contribute to our project effortlessly!

## Running the Project

1. **Setup the Environment:**

    To get started, set up the necessary environment variables. Create a `.env` file in your project root and define your secrets. For instance, if you're using a `SECRET_KEY`, ensure it's defined there.

2. **Running the Server:**

    Run the server using the following command:

    ```bash
    python manage.py runserver
    ```

    Access the development server at `http://localhost:8000/` in your browser.

## Dependencies and Packages

We leverage various packages in our Django project:

```python
# Example imports of some used packages
import django
import pandas as pd

[[package]]
name = "asgiref"
version = "3.5.1"
description = "ASGI specs, helper code, and adapters"
category = "main"
optional = false
python-versions = ">=3.7"

[package.extras]
tests = ["pytest", "pytest-asyncio", "mypy (>=0.800)"]

[[package]]
name = "django"
version = "3.2.13"
description = "A high-level Python Web framework that encourages rapid development and clean, pragmatic design."
category = "main"
optional = false
python-versions = ">=3.6"

[package.dependencies]
asgiref = ">=3.3.2,<4"
pytz = "*"
sqlparse = ">=0.2.2"

[package.extras]
argon2 = ["argon2-cffi (>=19.1.0)"]
bcrypt = ["bcrypt"]

[[package]]
name = "pytz"
version = "2022.1"
description = "World timezone definitions, modern and historical"
category = "main"
optional = false
python-versions = "*"

[[package]]
name = "sqlparse"
version = "0.4.2"
description = "A non-validating SQL parser."
category = "main"
optional = false
python-versions = ">=3.5"

[metadata]
lock-version = "1.1"
python-versions = "^3.8"
content-hash = "258c756954908c648e7416565d2696cc0e68284931f1dfc9b8d60e0325321315"

[metadata.files]
asgiref = [
    {file = "asgiref-3.5.1-py3-none-any.whl", hash = "sha256:45a429524fba18aba9d512498b19d220c4d628e75b40cf5c627524dbaebc5cc1"},
    {file = "asgiref-3.5.1.tar.gz", hash = "sha256:fddeea3c53fa99d0cdb613c3941cc6e52d822491fc2753fba25768fb5bf4e865"},
]
django = [
    {file = "Django-3.2.13-py3-none-any.whl", hash = "sha256:b896ca61edc079eb6bbaa15cf6071eb69d6aac08cce5211583cfb41515644fdf"},
    {file = "Django-3.2.13.tar.gz", hash = "sha256:6d93497a0a9bf6ba0e0b1a29cccdc40efbfc76297255b1309b3a884a688ec4b6"},
]
pytz = [
    {file = "pytz-2022.1-py2.py3-none-any.whl", hash = "sha256:e68985985296d9a66a881eb3193b0906246245294a881e7c8afe623866ac6a5c"},
    {file = "pytz-2022.1.tar.gz", hash = "sha256:1e760e2fe6a8163bc0b3d9a19c4f84342afa0a2affebfaa84b01b978a02ecaa7"},
]
sqlparse = [
    {file = "sqlparse-0.4.2-py3-none-any.whl", hash = "sha256:48719e356bb8b42991bdbb1e8b83223757b93789c00910a616a071910ca4a64d"},
    {file = "sqlparse-0.4.2.tar.gz", hash = "sha256:0c00730c74263a94e5a9919ade150dfc3b19c574389985446148402998287dae"},
]
