import os
import click

from praetorian_cli.handlers.utils import chariot
from praetorian_cli.handlers.utils import Status
from praetorian_cli.handlers.utils import handle_api_error


@chariot.command('seeds')
@click.pass_obj
@handle_api_error
@click.option('-seed', '--seed', default="", help="Filter by seed domain")
def my_seeds(controller, seed):
    """ Fetch seed domains """
    result = controller.my(dict(key=f'#seed#{seed}'))
    for hit in result.get('seeds', []):
        print(f"{hit['key']}")


@chariot.command('assets')
@click.pass_obj
@handle_api_error
@click.option('-seed', '--seed', default="", help="Filter by seed domain")
def my_assets(controller, seed):
    """ Fetch existing assets """
    result = controller.my(dict(key=f'#asset#{seed}'))
    for hit in result.get('assets', []):
        print(f"{hit['key']}")


@chariot.command('risks')
@click.pass_obj
@handle_api_error
@click.option('-seed', '--seed', default="", help="Filter by seed domain")
def my_risks(controller, seed):
    """ Fetch current risks """
    result = controller.my(dict(key=f'#risk#{seed}'))
    for hit in result.get('risks', []):
        print(f"{hit['key']}")


@chariot.command('technology')
@click.pass_obj
@handle_api_error
@click.option('-seed', '--seed', default="", help="Filter by seed domain")
def my_technology(controller, seed):
    """ Fetch recently seen technology """
    result = controller.my(dict(key=f'#tech#{seed}'))
    for hit in result.get('technology', []):
        print(f"{hit['key']}")


@chariot.command('jobs')
@click.pass_obj
@handle_api_error
@click.option('-updated', '--updated', default="", help="Fetch jobs since date")
def my_jobs(controller, updated):
    """ Fetch past, present and future jobs """
    result = controller.my(dict(key=f'#job#{updated}'))
    for hit in result.get('jobs', []):
        print(f"{hit['key']}")


@chariot.command('files')
@click.pass_obj
@handle_api_error
@click.option('-name', '--name', default="", help="Filter by relative path")
def my_files(controller, name):
    """ Fetch all file names """
    result = controller.my(dict(key=f'#file#{name}'))
    for hit in result.get('files', []):
        print(f"{hit['key']}")


@chariot.command('threats')
@click.pass_obj
@handle_api_error
@click.option('-source', '--source', type=click.Choice(['KEV']), default="KEV", help="Filter by threat source")
def my_threats(controller, source):
    """ Fetch threat intelligence """
    result = controller.my(dict(key=f'#threat#{source}'))
    for hit in result.get('threats', []):
        print(f"{hit['key']}")


@chariot.command('add-seed')
@click.pass_obj
@handle_api_error
@click.argument('seed')
@click.option('-status', '--status', type=click.Choice(['AS', 'FS']), required=False, default="AS")
@click.option('-comment', '--comment', default="", help="Add a comment")
def add_seed(controller, seed, status, comment=""):
    """ Add a new seed """
    controller.add_seed(seed, status=status, comment=comment)


@chariot.command('delete-seed')
@click.pass_obj
@handle_api_error
@click.argument('seed')
def delete_seed(controller, seed):
    """ Delete any seed """
    controller.delete_seed(f'#seed#{seed}')


@chariot.command('update-seed')
@click.pass_obj
@handle_api_error
@click.argument('key')
@click.option('-status', '--status', type=click.Choice(['AS', 'FS']), required=False, default="AS")
@click.option('-comment', '--comment', help="Add a comment")
def update_seed(controller, key, status, comment=''):
    """ Update any seed """
    controller.update_seed(key, status=status, comment=comment)


@chariot.command('add-asset')
@click.pass_obj
@handle_api_error
@click.option('-seed', '--seed', required=True)
@click.option('-dns', '--dns', required=True)
@click.option('-name', '--name', required=True)
def add_asset(controller, seed, dns, name):
    """ Update any asset """
    controller.add_asset(seed=seed, dns=dns, name=name)


@chariot.command('update-asset')
@click.pass_obj
@handle_api_error
@click.argument('key')
@click.option('-status', '--status', type=click.Choice(['AA', 'FA']), required=False, default="AA")
@click.option('-comment', '--comment', help="Add a comment")
def update_asset(controller, key, status, comment=''):
    """ Update any asset """
    controller.update_asset(key, status=status, comment=comment)


@chariot.command('add-risk')
@click.pass_obj
@handle_api_error
@click.argument('key')
@click.option('-name', '--name', required=True, help="Generic risk identifier")
@click.option('-status', '--status', type=click.Choice([s.value for s in Status]), required=False, default='TO')
@click.option('-comment', '--comment', help="Add a comment")
def add_risk(controller, key, name, status, comment):
    """ Apply a risk to an asset key """
    print(controller.add_risk(key, name, status, comment))


@chariot.command('update-risk')
@click.pass_obj
@handle_api_error
@click.argument('key')
@click.option('-name', '--name', required=False, help="Generic risk identifier")
@click.option('-status', '--status', type=click.Choice([s.value for s in Status]), required=False)
@click.option('-comment', '--comment', help="Add a comment")
def add_risk(controller, key, name, status, comment):
    """ Update an existing Risk key """
    print(controller.update_risk(key, name, status, comment))


@chariot.command('upload')
@click.pass_obj
@handle_api_error
@click.argument('name')
def upload(controller, name):
    """ Upload a file """
    controller.upload(name)


@chariot.command('download')
@click.pass_obj
@handle_api_error
@click.argument('key')
@click.argument('path')
def download(controller, key, path):
    """ Download any previous uploaded file """
    controller.download(key, path)


@chariot.command('search')
@click.pass_obj
@handle_api_error
@click.option('-term', '--term', help="Enter a search term")
@click.option('-count', '--count', is_flag=True, help="Return statistics on search")
def search(controller, term="", count=False):
    """ Query the data store for arbitrary matches """
    if count:
        print(controller.count(dict(key=term)))
    else:
        resp = controller.my(dict(key=term))
        for key, value in resp.items():
            if isinstance(value, list):
                for hit in value:
                    print(f"{hit['key']}")


@chariot.command('test')
@click.pass_obj
def trigger_all_tests(controller):
    """ Run integration test suite """
    try:
        import pytest
    except ModuleNotFoundError:
        print("Install pytest using 'pip install pytest' to run this command")
    test_directory = os.path.relpath("praetorian_cli/sdk/test", os.getcwd())
    pytest.main([test_directory])
