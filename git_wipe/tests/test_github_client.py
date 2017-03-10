# -*- coding: utf-8 -*-

import pytest
from mock import patch, Mock, MagicMock, PropertyMock
from click.testing import CliRunner

from git_wipe.cli import (cli, cleanup)
from git_wipe.__version__ import __version__
from github.GithubException import BadCredentialsException
from github.Repository import Repository
from github.Branch import Branch
from github.AuthenticatedUser import AuthenticatedUser
from git_wipe.github_client import GithubClient
from github import Github


class TestGithubClient():

    @patch('github.Repository.Repository')
    @patch('github.Github')
    def test_get_merged_fork_branches(self, mock_github, mock_repository):
        mock_get_user = mock_github.get_user
        mock_get_user.return_value.login = 'login'
        mock_get_repos = mock_get_user.return_value.get_repos

        mock_parent_repo = mock_github.get_repo
        mock_parent_repo.side_effect = self._get_mock_parent_repo

        mock_repo_1 = self._get_mock_repo('repo_1', True)
        mock_repo_1.get_branches.return_value = [
            self._get_mock_branch('master'),
            self._get_mock_branch('develop'),
            self._get_mock_branch('branch_1'),
            self._get_mock_branch('branch_2'),
            self._get_mock_branch('branch_3'),
        ]

        mock_get_repos.return_value = [
            mock_repo_1,
            self._get_mock_repo('repo_2', True),  # is in --skip-repository
            self._get_mock_repo('repo_3', False),  # is not fork
        ]
        github_client = GithubClient('token', 30)
        github_client._github = mock_github
        repo_branches = github_client.get_merged_fork_branches(
            ('repo_2'), ('develop'))

        assert 2 == len(repo_branches)
        for repo, branch in repo_branches:
            assert repo.name == 'repo_1'
            assert branch.name in ['branch_1', 'branch_2']

        mock_github.get_repo.assert_called_with('repo_1')
        mock_get_repos.assert_called_with(type='owner')

    @patch('github.Github')
    def test_delete_branches(self, mock_github):
        mock_repo_1 = self._get_mock_repo('repo_1')
        mock_repo_1.get_git_ref.side_effect = self._get_mock_git_ref
        mock_repo_1_branch_1 = self._get_mock_branch('branch_1')
        repo_branches = [
            [
                mock_repo_1,
                mock_repo_1_branch_1
            ]
        ]

        github_client = GithubClient('token', 30)
        github_client.delete_branches(repo_branches)

    def _get_mock_repo(self, name, is_fork=True):
        with patch('github.Repository.Repository') as mock_repository:
            mock_repository.name = name
            mock_repository.fork = is_fork
            mock_repository.parent.id = name

        return mock_repository

    def _get_mock_pull_request(self, head, state):
        assert state == 'closed'
        assert head in ['login:branch_1', 'login:branch_2', 'login:branch_3']
        with patch('github.PullRequest.PullRequest') as mock_pull_request:
            mock_pull_request.is_merged.return_value = head in [
                'login:branch_1', 'login:branch_2']

        return [mock_pull_request]

    def _get_mock_parent_repo(self, id):
        with patch('github.Repository.Repository') as mock_parent_repository:
            mock_parent_repository.get_pulls.side_effect = self._get_mock_pull_request

        return mock_parent_repository

    def _get_mock_branch(self, name):
        with patch('github.Branch.Branch') as mock_branch:
            mock_branch.name = name

        return mock_branch

    def _get_mock_git_ref(self, ref):
        assert ref == 'heads/branch_1'

        with patch('github.GitRef.GitRef') as mock_git_ref:
            return mock_git_ref
