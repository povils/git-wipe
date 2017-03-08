# -*- coding: utf-8 -*-

import pytest
from mock import patch, Mock
from click.testing import CliRunner

from git_wipe.cli import (cli, cleanup)
from git_wipe.__version__ import __version__
from github.GithubException import BadCredentialsException
from git_wipe.github_client import GithubClient

class TestCli():

    def test_cli_without_invoked_subcommand(self):
       runner = CliRunner()
       result = runner.invoke(cli)

       assert result.exit_code == 0
       for string in ['--help' ,'--version', 'cleanup', 'Options', 'Commands']:
           assert string in result.output

    def test_cli_with_version_option(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])

        assert result.exit_code == 0
        assert result.output == 'git-wipe, version ' + __version__ + '\n'


    def test_cli_cleanup_wihout_any_options(self):
        runner = CliRunner()
        result = runner.invoke(cleanup, input = 'token')

        assert 'Please enter your Github access token' in result.output

    @patch.object(GithubClient, 'get_merged_fork_branches')
    def test_cli_cleanup_with_invalid_token_option(self, get_merged_fork_branches):
        get_merged_fork_branches.side_effect = BadCredentialsException('Bad Credentials' ,'test')
        runner = CliRunner()
        result = runner.invoke(cleanup, ['--token=token'])

       # get_merged_fork_branches.assert_called_with((), ())
        assert result.exit_code == 1
        assert 'Bad credentials' in result.output

    @patch.object(GithubClient, 'get_merged_fork_branches')
    def test_cli_cleanup_with_skip_options(self, get_merged_fork_branches):
        get_merged_fork_branches.return_value = []
        runner = CliRunner()
        options = [
            '--token=token',
            '--skip-repository=repository_1',
            '--skip-repository=repostiory_2',
            '--skip-branch=branch_1',
            '--skip-branch=branch_2',
        ]
        result = runner.invoke(cleanup, options)
        print(result.output)
        #get_merged_fork_branches.assert_called_with(('repository_1', 'repository_2'), ('branch_1', 'branch_2'))
        get_merged_fork_branches.assert_called_with(('repository_1', 'repository_2'), 'b')


