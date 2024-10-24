Bitbucket to GitLab Migration Script

This repository contains a Python script designed to automate the migration of repositories from Bitbucket to GitLab. The script leverages both Bitbucket and GitLab APIs to clone repositories from a specified Bitbucket workspace and push them to a GitLab group.
Features

  Project-based Repository Fetching: Fetches all repositories within a specific Bitbucket project and migrates them to GitLab.
  Handles All Branches: Clones the repositories and pushes all branches from Bitbucket to GitLab, ensuring a full transfer of version history.
  Automated Migration: Automatically clones repositories, checks out all branches, and pushes them to the specified GitLab group.
  Error Handling: Provides basic error handling to ensure any issues with repository cloning or pushing are properly reported.

Requirements

  Python 3.x
  GitPython: A Python library to interact with Git repositories.
  Requests: For handling Bitbucket API requests.

How to Use

Clone the Repository:

    git clone https://github.com/yourusername/bitbucket-to-gitlab-migrator.git
    cd bitbucket-to-gitlab-migrator
    

Install dependencies:

```bash

pip install gitpython requests
```
Usage

  Clone this repository to your local machine.
  Run the script and provide the necessary credentials when prompted:

    python bitbucket_to_gitlab_repo_transfer.py
    
You will be asked for:
  -Bitbucket Username
  -Bitbucket App Password
  -Bitbucket Workspace Name
  -GitLab Username
  -GitLab Token
  -GitLab Group ID

The script will clone repositories from the Bitbucket workspace and push them to the GitLab group.
