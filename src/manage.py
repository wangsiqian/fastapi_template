from pathlib import Path

import alembic.config
import click
import uvicorn

from apps.base import create_app
from utils.config import get_config

app = create_app()
config = get_config()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """CLI management for FastAPI project
    """


@cli.command('start')
def start():
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        log_config=config.log_config()
    )


@cli.command('test')
@click.argument('test_names', required=False, nargs=-1)
def test(test_names):
    import pytest

    args = config.PYTEST_ARGS
    if test_names:
        args.extend(test_names)
    pytest.main(args)


@cli.command('migrate')
@click.argument('commit', required=False, nargs=-1)
def migrate(commit):
    path = Path('models/migrations', 'versions')
    if path.exists():
        has_versions = any(
            filter(lambda _dir: _dir.name.endswith('.py'), path.iterdir())
        )
    else:
        path.mkdir()
        has_versions = False

    revision_args = ['revision', '--autogenerate', '-m']
    if has_versions is False:
        revision_args.append('"init database."')
    else:
        if commit:
            revision_args.append(f'"{commit}"')
        else:
            revision_args.append('"update database."')

    alembic.config.main(argv=revision_args)

    migrate_args = ['--raiseerr', 'upgrade', 'head']
    alembic.config.main(argv=migrate_args)


if __name__ == '__main__':
    cli()
