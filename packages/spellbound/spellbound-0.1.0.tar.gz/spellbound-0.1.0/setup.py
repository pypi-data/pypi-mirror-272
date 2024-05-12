"""Python setup.py for spellbound package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("spellbound", "VERSION")
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


cli_extra_requires = ["typer>=0.12.0", "rich[jupyter]"]

setup(
    name="spellbound",
    version=read("spellbound", "VERSION"),
    description="Spell framework",
    url="https://github.com/kristw/spellbound/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="kristw",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=[
        "cached-property",
        "pydantic<2",
        "typing_extensions",
    ],
    extras_require={
        "test": [
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
        ]
        + cli_extra_requires,
        "cli": cli_extra_requires,
    },
)
