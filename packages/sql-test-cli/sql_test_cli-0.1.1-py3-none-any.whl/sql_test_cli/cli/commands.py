import click
import colorama

from sql_test_cli.core.run import run
from sql_test_cli.core.initialize import init

colorama.init()

@click.group
def my_commands():
    pass

my_commands.add_command(run)
my_commands.add_command(init)

            
if __name__ == "__main__":
    my_commands()
