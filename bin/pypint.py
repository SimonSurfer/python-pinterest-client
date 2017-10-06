import logging
import os
import click
import json

from pinterest.client import PintClient


def configure_logging(debug=False):
    fmt = '%(asctime)s %(levelname)-7s [%(name)s] %(message)s [%(filename)s:%(lineno)s]'
    logger = logging.getLogger('pinterest')
    formatter = logging.Formatter(fmt)
    logger.handlers = []
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

def print_resource(obj):
    click.echo('-- {resource} --'.format(resource=obj))
    for field in obj.namespace._meta['fields']:
        if hasattr(obj, field):
            value = getattr(obj, field)
            if isinstance(value, dict):
                click.echo(u'\- {field}:\n{value}'.format(field=field, value=json.dumps(value, sort_keys=True, indent=4)))
            else:
                click.echo(u'\- {field}: {value}'.format(field=field, value=value))


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    configure_logging(debug)
    ctx.obj = {}

    try:
        ctx.obj['CLIENT'] = PintClient(os.environ['PINT_ACCESS_TOKEN'])
    except KeyError:
        raise EnvironmentError('You need to add PINT_ACCESS_TOKEN environment variable')


@cli.group()
@click.argument('id')
@click.pass_context
def board(ctx, id):
    ctx.obj['BOARD'] = ctx.obj['CLIENT'].boards.get(id)

@board.command()
@click.pass_context
def show(ctx):
    print_resource(ctx.obj['BOARD'])

@board.command()
@click.pass_context
def pins(ctx):
    board = ctx.obj['BOARD']
    click.echo('-- board: {id} --'.format(id=board.id))
    for pin in board.get_pins():
        print pin

@cli.group()
@click.argument('id')
@click.pass_context
def pin(ctx, id):
    ctx.obj['PIN'] = ctx.obj['CLIENT'].pins.get(id)


@pin.command()
@click.pass_context
def show(ctx):
    print_resource(ctx.obj['PIN'])


if __name__ == '__main__':
    cli()


