import click
import logging
import yaml

from sql_test_cli.cli.outputs import init_cli, report_successful_project_initialization
from sql_test_cli.core.logger import configure_logger
from sql_test_cli.core.directory_check import *

from sql_test_cli.core.config_manager import retrieve_config_values

configure_logger()

logger = logging.getLogger(__name__)

URI, TARGET_DIR, LOG_LEVEL = retrieve_config_values()

@click.command()
def init():
    """Initialize a sql  test project directory."""
    
    cwd = os.getcwd()

    config_dict = {
        'uri' : '',
        'target_dir' : '',
        'log_level' : 'WARN',
        'app_env' : ''
    }

    if not os.path.exists(cwd + '/.sql-test-cli'):
        os.mkdir('.sql-test-cli')
        os.mkdir(cwd + '/.sql-test-cli/runs')

        with open('sql-test-cli.yaml', 'w') as file:
            yaml.dump(config_dict, file)

        with open('.gitignore', 'w') as fp:
            fp.write("venv/\n.env\n**/__pycache__/\n.sql-test-cli\nsql-test-cli.yaml")

        init_cli()
        report_successful_project_initialization(cwd)
        
    else:
        SystemExit(print('This directory has already initialized as a sql-test-cli directory.'))

