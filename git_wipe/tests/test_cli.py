# -*- coding: utf-8 -*-

import pytest
from mock import patch, Mock
from click.testing import CliRunner

from git_wipe.cli import (cli, cleanup)
from git_wipe.__version__ import __version__
from github.GithubException import BadCredentialsException
from github.Repository import Repository
from github.Branch import Branch
from git_wipe.github_client import GithubClient


class TestCli():

    def test_cli_without_invoked_subcommand(self):
        runner = CliRunner()
        result = runner.invoke(cli)

        assert result.exit_code == 0
        for string in ['--help', '--version', 'cleanup', 'Options', 'Commands']:
            assert string in result.output

    def test_cli_with_version_option(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])

        assert result.exit_code == 0
        assert result.output == 'git-wipe, version ' + __version__ + '\n'

    @patch.object(GithubClient, 'get_merged_fork_branches')
    def test_cli_cleanup_wihout_any_options(self, get_merged_fork_branches):
        get_merged_fork_branches.side_effect = []
        runner = CliRunner()
        result = runner.invoke(cleanup, input='token')

        assert 'Please enter your Github access token' in result.output

    @patch.object(GithubClient, 'get_merged_fork_branches')
    def test_cli_cleanup_with_invalid_token_option(self, get_merged_fork_branches):
        get_merged_fork_branches.side_effect = BadCredentialsException(
            'Bad Credentials', 'test')
        runner = CliRunner()
        result = runner.invoke(cleanup, ['--token=token'])

        get_merged_fork_branches.assert_called_with((), ())
        assert result.exit_code == 1
        assert 'Bad credentials' in result.output

    @patch.object(GithubClient, 'get_merged_fork_branches')
    def test_cli_cleanup_with_skip_options(self, get_merged_fork_branches):
        get_merged_fork_branches.return_value = []
        runner = CliRunner()
        options = [
            '--token=token',
            '--skip-repository=repository_1',
            '--skip-repository=repository_2',
            '--skip-branch=branch_1',
            '--skip-branch=branch_2',
        ]
        result = runner.invoke(cleanup, options)
        get_merged_fork_branches.assert_called_with(
            ('repository_1', 'repository_2'), ('branch_1', 'branch_2'))
        assert 'Congratulations' in result.output

    @patch('github.Repository.Repository')
    @patch('github.Branch.Branch')
    @patch.object(GithubClient, 'get_merged_fork_branches')
    @patch.object(GithubClient, 'delete_branches')
    def test_cli_cleanup_list_find_branches_and_ask_to_delete(self, delete_branches, get_merged_fork_branches, mocked_branch, mocked_repository):
        mocked_repository.full_name = 'repo_name'
        mocked_branch.name = 'branch_name'
        repo_branches = [
            [mocked_repository, mocked_branch]
        ]

        get_merged_fork_branches.return_value = repo_branches

        runner = CliRunner()
        options = [
            '--token=token',
        ]

        result = runner.invoke(cleanup, options, input='y')
        delete_branches.assert_called_with(repo_branches)
        assert 'Searching' in result.output
        assert 'repo_name:branch_name' in result.output
        assert 'Delete these branches?' in result.output
        assert 'Deleting branches' in result.output
        assert 'Done' in result.output

    @patch('github.Repository.Repository')
    @patch('github.Branch.Branch')
    @patch.object(GithubClient, 'get_merged_fork_branches')
    @patch.object(GithubClient, 'delete_branches')
    def test_cli_cleanup_with_preview_option_should_not_ask_to_delete(self, delete_branches, get_merged_fork_branches, mocked_branch, mocked_repository):
        mocked_repository.full_name = 'repo_name'
        mocked_branch.name = 'branch_name'
        repo_branches = [
            [mocked_repository, mocked_branch]
        ]
        get_merged_fork_branches.return_value = repo_branches

        runner = CliRunner()
        options = [
            '--token=token',
            '--preview',
        ]

        result = runner.invoke(cleanup, options)

        assert 'Delete these branches?' not in result.output
        assert 'Deleting branches' not in result.output
        assert not delete_branches.called
