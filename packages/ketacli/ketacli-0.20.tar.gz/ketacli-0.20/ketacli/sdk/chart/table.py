from rich.console import Console
from ketacli.sdk.output.format import OutputTable
from rich.table import Table
from rich.panel import Panel

class KTable:
    def __init__(self, data: OutputTable, title=None, ):
        self.data = data
        self.title = title

    def __rich_console__(self, console, options):
        width = options.max_width or console.width
        self.height = options.height or console.height
        table = Table(show_header=True, header_style="bold magenta", width=width, expand=True, padding=0, show_lines=True)
        for column in self.data.header:
            table.add_column(column, style="blink", justify="center")
        for row in self.data.rows:
            row = [str(i) for i in row]
            table.add_row(*row)
        panel = Panel(table, expand=True, padding=0, title=self.title, height=self.height)
        yield panel


if __name__ == '__main__':
    console = Console()
    table = OutputTable(["main", "res", "shard", "pc"], [[1, 2, 3, 100]])
    console.print(KTable(table, title="title", ))
