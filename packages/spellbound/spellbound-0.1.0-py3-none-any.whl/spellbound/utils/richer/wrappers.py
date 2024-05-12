class Markdown(str):
    """Wrapper of a str to hint that the string is a markdown"""

    @classmethod
    def list(cls, iterable):
        return cls(("* " + "\n* ".join(iterable)))

    @classmethod
    def diff(cls, diff_string):
        return cls(f"```diff\n{diff_string}\n```")


class Markup(str):
    """Wrapper of a str to hint that the string is a rich markup"""


class RenderableList(list):
    """
    Wrapper of a list to hint that each item in the list
    should be check if it is renderable by richer
    """


class Syntax:
    """Wrapper of a str to hint that the string is a syntax string"""

    def __init__(self, code, language):
        self.code = code
        self.language = language
