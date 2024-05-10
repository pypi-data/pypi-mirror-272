from cgi import test
import click
from dotenv import load_dotenv
import logging

from sql_test_cli.core.connection import create_connection
from sql_test_cli.cli.outputs import init_cli, report_file_count, report_test_start
from sql_test_cli.core.directory_check import *
from sql_test_cli.core.run_test import handle_test_result, read_sql_file, run_sql_test

from sql_test_cli.core.config import config_check
from sql_test_cli.core.config_manager import retrieve_config_values

@click.command()
@click.option('--uri', help='A sqlalchemy URI that will override the URI provided in .env.')
@click.option('--target_dir', help='The target directory in which run sql-test-cli. Default is the current directory from which the sql-test-cli command is run.')
@click.option('--filepath', help='A path to a single sql  test file.')
def run(uri, target_dir, filepath):
    """Execute sql  tests, 'sql-test-cli run --help' for options."""

    URI, TARGET_DIR, _ = retrieve_config_values()

    init_cli()

    if not uri:
        uri = URI

    config_check(uri, target_dir, filepath)


    if not filepath:
        files_list = check_directory(TARGET_DIR)

        report_file_count(files_list)

        for i, f in enumerate(files_list):

            report_test_start(index=i, filename=f)
            
            test_sql, test_file_path = read_sql_file(test_file_path=TARGET_DIR + '/' + f)

            con = create_connection(uri)

            test_result_df, test_duration = run_sql_test(test_sql=test_sql, con=con)

            handle_test_result(test_result_df=test_result_df, test_duration=test_duration, test_filename=f, test_file_path=test_file_path)
    
    else:
        files_list = [filepath]

        report_file_count(files_list)

        report_test_start(filename=filepath)
            
        test_sql, test_file_path = read_sql_file(test_file_path=filepath)

        con = create_connection(uri)

        test_result_df = run_sql_test(test_sql=test_sql, con=con)

        handle_test_result(test_result_df=test_result_df, test_duration=test_duration, test_filename=filepath, test_file_path=test_file_path)
