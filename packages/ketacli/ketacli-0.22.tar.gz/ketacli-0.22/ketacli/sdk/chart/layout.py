from rich import print
from rich.layout import Layout


def create_layout(rows, cols, layout_configs=None):
    if layout_configs is None:
        layout_configs = {}
    root = Layout(name="root")
    row_layouts = []
    for i in range(rows):
        row_layout = Layout(name=f"row{i}", **layout_configs.get(f'row{i}', {}))
        row_layouts.append(row_layout)
        column_layouts = []
        for j in range(cols):
            col_config = layout_configs.get(f'row{i}-col{j}', {})
            if col_config:
                size = col_config.get("size", None)
                ratio = col_config.get("ratio", None)
                if not size and not ratio:
                    continue
            column_layout = Layout(name=f"row{i}-col{j}", **col_config)
            column_layouts.append(column_layout)
        row_layout.split_row(*column_layouts)
    root.split_column(*row_layouts)
    return root


if __name__ == '__main__':
    configs = {
        "row0": {"size": 0, "ratio": 2},
        "row4": {"size": 0, "ratio": 3},
        "row0-col0": {"size": 0, "ratio": 2},
        "row1-col1": {"size": 0, "ratio": 1},
    }

    layout = create_layout(5, 3, configs)
    print(layout)
