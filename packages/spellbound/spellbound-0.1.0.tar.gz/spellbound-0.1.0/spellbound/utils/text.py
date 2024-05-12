import re

# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
_first_pass_re = re.compile("([^_])([A-Z][a-z]+)")
_second_pass_re = re.compile("([a-z0-9])([A-Z])")

def snake_case(name):
    """Return string as snake_case."""
    name = re.sub(_first_pass_re, r"\1_\2", name)
    return re.sub(_second_pass_re, r"\1_\2", name).lower()

def camel_case(name):
    """Return string as CamelCase"""
    return re.sub(r"(_|-)+", " ", snake_case(name)).title().replace(" ", "")

def kebab_case(name):
    """Return string as kebab-case"""
    return re.sub(r"(_|-)+", "-", snake_case(name))

def title_case(name):
    """Return string as Title Case"""
    return re.sub(r"(_|-)+", " ", snake_case(name)).title()

