"""Python setup.py for yamlsql package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("yamlsql", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="yamlsql",
    version=read("yamlsql", "VERSION"),
    description="Awesome yamlsql created by kristw",
    url="https://github.com/kristw/yamlsql/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="kristw",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[
        "fastapi",
        "fastapi-crudrouter",
        "sqlalchemy",
        "pydantic",
    ],
    entry_points={
        "console_scripts": ["yamlsql = yamlsql.__main__:main"]
    },
    extras_require={"test": [
        "autoflake==1.5.3",
        "black==22.6.0",
        "coverage",
        "gitchangelog",
        "isort",
        "mkdocs",
        "mypy",
        "pre-commit",
        "poetry",
        "pytest",
        "pytest-cov",
    ]},
)
