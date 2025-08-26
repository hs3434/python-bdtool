from string import Formatter
import sys
import re
import click
import pandas as pd
from bdtool.share import color_map

@click.group()
def cli():
    """Command-line toolset for bdtool."""
    pass 

def get_formatter_keys(ss: str):
    res = set()
    for t in Formatter().parse(ss):
        if t[1] is not None:
            res.add(t[1])
    return res

@cli.command()
@click.argument("file_path")
def touch(file_path):
    """
    Create <FILE_PATH>, or update the access and modification time if it already exists.
    """
    with open(file_path, 'a') as f:
        pass

def common_color_rgb(color) -> tuple | None:
    if isinstance(color, str):
        if color in color_map:
            return color_map[color]
        else:
            match = re.search(r"\(([^>]+)\)", color)
            if match:
                rgb = tuple(int(v) for v in match.group(1).split(','))
                if len(rgb) >= 3:
                    return rgb
            return None
    else:
        return tuple(int(v) for v in color)

@cli.command()
@click.argument("file_path")
@click.option("-n", "--num", help="Number of lines")
@click.option("-p", "--print", is_flag=True, help="only print result")
def check_row_num(file_path, num, print):
    """
    Check if the table in <FILE_PATH> has enough rows.
    """
    df = pd.read_csv(file_path)
    if df.shape[0] < num:
        if print:
            click.echo(f"{file_path} has {df.shape[0]} rows, less than {num}")
        else:
            raise click.ClickException(f"{file_path} has {df.shape[0]} rows, less than {num}")
    