#!/usr/bin/env python3
from config import settings
import click
from linkedin_api import Linkedin

@click.group()
@click.option('-u', '--li-username', 'username', default=settings.linkedin_username, type=str,
        help="Username for your LinkedIn account")
@click.option('-p', '--li-password', 'password',
        default=settings.linkedin_password, type=str,
        help='Password for your LinkedIn account')
@click.option('-v', '--verbose', 'verbose',
        default=False, type=bool,
        help='Increase verbosity')
@click.pass_context
def cli(ctx, username, password, verbose):
    """Run commands against a LinkedIn account"""
    ctx.ensure_object(dict)
    #ctx.obj['username'] = username
    #ctx.obj['password'] = password
    ctx.obj['verbose'] = verbose
    ctx.obj['api'] = Linkedin(username, password, debug=verbose)

@cli.command()
@click.pass_context
def show_profile(ctx):
    """Show connected LinkedIn Profile"""
    api = ctx.obj['api']

@cli.command()
@click.pass_context
def get_conversations(ctx):
    """Show conversations active in connected LinkedIn Profile"""
    api = ctx.obj['api']
    click.echo(api.get_conversations())


if __name__ == "__main__":
    cli(obj={})
