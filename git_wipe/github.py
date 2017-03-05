from github import Github as PyGithub
from github.GithubException import BadCredentialsException

class Github:

    def create(self, token, timeout):
        self._py_github = PyGithub(login_or_token=token, timeout=timeout)

        return self
    
    def get_merged_fork_branches(self, skip_repository, skip_branch):
        count = 0
        repo_branches = []
        user = self._py_github.get_user()
        for repo in user.get_repos(type='owner'):
            if repo.name not in skip_repository and repo.fork:
                parent_repo = self._py_github.get_repo(repo.parent.id)
                for branch in repo.get_branches():
                    if branch.name != 'master' and branch.name not in skip_branch:
                        for pull in parent_repo.get_pulls(head=user.login + ':' + branch.name, state="closed"):
                            if pull.is_merged():
                                repo_branches.append([repo, branch])

        return repo_branches

    def delete_branches(self, repo_branches):
        for repo, branch in repo_branches:
            repo.get_git_ref('heads/' + branch.name).delete()
