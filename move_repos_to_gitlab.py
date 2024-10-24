import os
import shutil
import git
import requests

# Bitbucket and GitLab configuration for testing
BITBUCKET_USERNAME = 'vipinsingh0102'
BITBUCKET_PASSWORD = "ATBBmBNpvQNtyRkCGSXuGrvtXyks1F01412D"
BITBUCKET_WORKSPACE = 'artivatic-official'
BITBUCKET_BASE_URL = f'git@bitbucket.org:{BITBUCKET_WORKSPACE}/'

GITLAB_USERNAME = 'navkaransinghhunjan'  # Testing GitLab username
GITLAB_TOKEN = 'glpat-77VswypgqjKyT4LRPa3E'  # GitLab token for testing
GITLAB_GROUP_ID = 'practice0071'  # Group ID for testing
GITLAB_API_URL = 'https://gitlab.com/api/v4/projects'  # API URL for testing GitLab


def get_repos_in_group(bitbucket_username, app_password, workspace, project_key):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}?q=project.key=\"{project_key}\""

    response = requests.get(url, auth=(bitbucket_username, app_password))

    if response.status_code == 200:
        data = response.json()
        repo_names = [repo['name'] for repo in data['values']]
        return repo_names
    else:
        print(f"Error: {response.status_code}")
        return []


def get_projects(bitbucket_username, app_password, workspace):
    url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/projects"

    response = requests.get(url, auth=(bitbucket_username, app_password))

    if response.status_code == 200:
        data = response.json()
        projects = data['values']
        project_keys = [project['key'] for project in projects]
        return project_keys
    else:
        print(f"Error: {response.status_code}")
        return {}


repos_list = []


def generate_repo_names():
    for project in get_projects(BITBUCKET_USERNAME, BITBUCKET_PASSWORD, BITBUCKET_WORKSPACE):
        repos_list.extend(
            get_repos_in_group(BITBUCKET_USERNAME, BITBUCKET_PASSWORD, BITBUCKET_WORKSPACE, project_key=project))
    return repos_list


def clone_and_push_repo(repo_name):
    repo_path = f'/tmp/repo_transfer/{repo_name}'
    try:
        if os.path.exists(repo_path):
            print(f'Directory {repo_path} already exists. Removing it...')
            shutil.rmtree(repo_path)

        bitbucket_repo_url = f'{BITBUCKET_BASE_URL}{repo_name}.git'
        print(f'Cloning {bitbucket_repo_url} to {repo_path}...')
        repo = git.Repo.clone_from(bitbucket_repo_url, repo_path)

        print('Fetching all branches...')
        repo.git.fetch('--all')

        gitlab_repo_url = f'git@gitlab.com:{GITLAB_GROUP_ID}/{repo_name}.git'  # GitLab repo URL for testing
        repo.create_remote('gitlab', gitlab_repo_url)

        # Checkout all the remote branches
        for branch in repo.git.branch('-r').splitlines():
            branch_name = branch.strip().split('/')[-1]  # Get the branch name
            if branch_name not in ['HEAD']:
                repo.git.checkout(branch_name)
                print(f'Checking out branch {branch_name}...')

        branches = [(ref.name).replace('origin/', '') for ref in repo.references]

        print(f'Branches to push: {branches}')

        for branch in set(branches):
            if not branch in ['HEAD']:
                repo.git.push('gitlab', branch)
                print(f'Pushing branch {branch} to GitLab...')

        print('Repository pushed to GitLab successfully.')

    except Exception as e:
        print(f'Failed to clone or push repository: {e}')


def migrate_bitbucket_to_gitlab():
    repo_names = generate_repo_names()
    for repo_name in repo_names:
        clone_and_push_repo(repo_name)


if __name__ == "__main__":
    migrate_bitbucket_to_gitlab()
