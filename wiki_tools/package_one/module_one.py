"""
    Application module.
"""
from wiki_tools import settings
from wiki_tools.package_two import module_two


def get_setting():
    return settings.filename


def add(x, y):
    """Add two numbers using a library."""
    return module_two.add_two_numbers(x, y)


def multiply(x, y):
    """Multiply two numbers using a library."""
    return module_two.multiply_two_numbers(x, y)


def raise_exception():
    """Raise an exception."""
    raise SystemExit(1)


class Calculator(object):
    class_field = "class_value"

    def __init__(self, instance_value):
        self.instance_field = instance_value

    def multiply(self, a, b):
        return a * b
