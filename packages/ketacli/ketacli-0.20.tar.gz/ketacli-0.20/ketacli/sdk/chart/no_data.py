from rich.table import Text
from rich.panel import Panel


class NoDataChart:
    def __init__(self, title=None, ):
        self.title = title

    def __rich_console__(self, console, options):
        width = options.max_width or console.width
        self.height = options.height or console.height
        texts = ((f"No data for chart \"{self.title}\"", "bold red"),)
        padding = (self.height - 4) // 2
        panel = Panel(Text.assemble(*texts, justify="center"), expand=True, padding=padding,
                      title=self.title, height=self.height)
        yield panel


if __name__ == '__main__':
    from rich.console import Console
    console = Console()
    console.print(NoDataChart(title="title", ))
