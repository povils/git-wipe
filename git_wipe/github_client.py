from github import Github


class GithubClient:

    def __init__(self, token, timeout):
        self._github = Github(login_or_token=token, timeout=timeout)

    def get_merged_fork_branches(self, skip_repository, skip_branch):
        repo_branches = []
        user = self._github.get_user()
        for repo in user.get_repos(type='owner'):
            if repo.name not in skip_repository and repo.fork:
                parent_repo = self._github.get_repo(repo.parent.id)
                for branch in repo.get_branches():
                    if branch.name != 'master' and branch.name not in skip_branch:
                        for pull in parent_repo.get_pulls(head=user.login + ':' + branch.name, state="closed"):
                            if pull.is_merged():
                                repo_branches.append([repo, branch])
                                break

        return repo_branches

    def delete_branches(self, repo_branches):
        for repo, branch in repo_branches:
            repo.get_git_ref('heads/' + branch.name).delete()
