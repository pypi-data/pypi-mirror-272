from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from ketacli.sdk.output.format import OutputTable


class SingleValueChart:
    def __init__(self, data: OutputTable, single_field, title=None, extra_fields: list = None, suffix="", prefix=""):
        self.data = data
        self.single_field = single_field
        self.title = title
        self.extra_fields = extra_fields
        self.suffix = suffix
        self.prefix = prefix

    def __rich_console__(self, console, options):
        width = options.max_width or console.width
        self.height = options.height or console.height
        single_value = self.prefix + [str(x[self.data.header.index(self.single_field)]) for x in self.data.rows][
            0] + self.suffix
        extra_values = []
        if self.extra_fields:
            for extra_field in self.extra_fields:
                extra_values.append(
                    f"{extra_field}: {[str(x[self.data.header.index(extra_field)]) for x in self.data.rows][0]}")
        extra_value = "\n".join(extra_values)
        padding = (int(self.height) - (len(self.extra_fields) + 1)) // 2
        texts = ((single_value, "bold magenta"), "\n", extra_value)
        panel = Panel(Text.assemble(*texts, justify="center"), expand=True, padding=padding, title=self.title)
        yield panel


if __name__ == '__main__':
    console = Console()
    table = OutputTable(["main", "res", "shard", "pc"], [[1, 2, 3, 100]])
    console.print(SingleValueChart(table, "pc", title="title", extra_fields=["main", "res", "shard"]))
