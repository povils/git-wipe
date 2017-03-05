import click
import crayons
import blindspin
import sys
import os
 
from .__version__ import __version__
from .env import GIT_WIPE_TOKEN
from .github import Github 
from github.GithubException import BadCredentialsException

@click.group(invoke_without_command=True)
@click.option('--help', is_flag=True, default=None, help='Show this message then exit.')
@click.version_option(prog_name=crayons.yellow('git-wipe'), version=__version__)
@click.pass_context
def cli(ctx, help):
    if ctx.invoked_subcommand is None:
        """CLI tool for deleting Github branches"""
        click.echo(ctx.get_help())

@click.command(help='Cleanup your remote merged branches as Pull Requests')
@click.option('--timeout', default=30, help='Set max timeout in seconds')
@click.option('--token', default=GIT_WIPE_TOKEN, help='Github Access Token')
@click.option('--skip-repository', multiple=True, help='Skip certain repositories')
@click.option('--skip-branch', multiple=True, help='Skip certain branches')
@click.option('--preview', is_flag=True, default=False, help='Preview found branches')
@click.option('--no-interaction', is_flag=True, default=False, help='Do not ask any interactive question')
def cleanup(token, timeout, skip_repository, skip_branch, preview, no_interaction):
    if token is None:
        token = click.prompt(crayons.green('Please enter your Github access token'))
   
    github = Github().create(token, timeout)
    try:
        click.echo(crayons.green('Searching for branches. This may take a while...'), err=True)
        with blindspin.spinner():
            repo_branches = github.get_merged_fork_branches(skip_repository, skip_branch)
    except BadCredentialsException:
        click.echo(crayons.red('Bad credentials. Please provide valid access token'), err=True)
        sys.exit(1)

    if not repo_branches:
        click.echo(crayons.green('Congratulations! You have nothing to delete'))
        sys.exit(0)

    list_branches(repo_branches)
    
    if False == preview:
        if False == no_interaction:
            click.confirm(crayons.green('Delete these branches?'), abort=True)
        click.echo(crayons.green('Deleting branches...'))
        with blindspin.spinner():
            github.delete_branches(repo_branches)
        click.echo(crayons.green('Done'))

def list_branches(repo_branches):
    for repo, branch in repo_branches:
        click.echo(crayons.blue(repo.full_name + ':' + branch.name))
 
# Add commands
cli.add_command(cleanup)

if __name__ == '__main__':
    cli()
#
