import rich.box
from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from spellbound.core.result import SpellResult, SpellStatus
from spellbound.utils.richer.core.renderer import RichRenderer


def _as_rich_markdown(x):
    return Markdown(str(x))


def _as_rich_text(x):
    return Text(str(x))


class SpellResultRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return SpellResult

    def status_icon(self, status):
        if status == SpellStatus.SUCCESS:
            # ✅
            return ":white_check_mark:"
        if status == SpellStatus.FAILURE:
            # ⛔
            return ":no_entry:"
        if status == SpellStatus.ABORTED:
            # 💥
            return ":collision:"

        # 🍨
        return ":ice_cream:"

    def status_style(self, status):
        if status == SpellStatus.SUCCESS:
            return "bold green"
        if status == SpellStatus.FAILURE:
            return "bold red"
        if status == SpellStatus.ABORTED:
            return "red"

        return "gray"

    def __call__(self, value):
        rich_title = Text()
        rich_title.append(self.status_icon(value.status))
        rich_title.append(" ")
        rich_title.append(value.status, style=self.status_style(value.status))
        rich_title.append(": ")
        rich_title.append(value.get_title())
        if value.duration is not None:
            rich_title.append(f" (Took {value.duration:.3f}s)")

        summary = Panel(rich_title.markup, expand=False)

        results = []

        if value.description:
            rich_description = self.richer.render(value.description, _as_rich_markdown)
            results.append(rich_description)

        if value.data is not None:
            if len(results) > 0:
                results.append("")  # Add a blank line
            content = self.richer.render(value.data, _as_rich_text)
            results.append(content)

        items = [summary]
        if results:
            items.insert(
                0,
                Group(
                    Panel(
                        Group(*results),
                        title="Result",
                        box=rich.box.HORIZONTALS,
                        padding=(1, 0),
                    )
                ),
            )

        return Group(*items)
