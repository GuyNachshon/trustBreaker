import base64
import datetime
import json
import os
import shutil
import subprocess
import tempfile
import requests

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def _pull_shark(repo_name, username, github_token, user_email):
    branch_sha = github_create_branch("pull-shark", repo_name, username, github_token)
    github_create_commit(branch_sha, repo_name, username, user_email, github_token, "pull-shark", "pull-shark!")
    pr_number = github_create_pull_request("pull-shark", f"pull-shark!", "pull-shark", repo_name, username, github_token)
    github_merge_pull_request(pr_number, "pull-shark", f"pull-shark!", repo_name, username, github_token)
    github_delete_branch("pull-shark", repo_name, username, github_token)


def _pair_extraordinaire(repo_name, username, github_token, user_email):
    branch_sha = github_create_branch("pair-extraordinaire", repo_name, username, github_token)
    github_create_commit(branch_sha, repo_name, username, user_email, github_token, "pair-extraordinaire", f"pair-extraordinaire!\n\ncoauthored-by: {username} <{user_email}>")
    pr_number = github_create_pull_request("pair-extraordinaire", f"pair-extraordinaire!\n\ncoauthored-by: {username} <{user_email}>", "pair-extraordinaire", repo_name, username, github_token)
    github_merge_pull_request(pr_number, "pair-extraordinaire", f"pair-extraordinaire!\n\ncoauthored-by: {username} <{user_email}>", repo_name, username, github_token)
    github_delete_branch("pair-extraordinaire", repo_name, username, github_token)


def github_open_issue(repo_name, username, github_token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/issues"
    data = {
        "title": "Quick Draw",
        "body": "Getting You An Achievement",
        "assignees": [
            username
        ],
        "labels": [
            "bug"
        ]
    }

    headers = {
        "Authorization": f"Bearer {github_token}",
    }
    issue_result = requests.post(url, data=json.dumps(data), headers=headers)
    issue_result = issue_result.json()
    return issue_result["number"]


def github_close_issue(issue_number, repo_name, username, github_token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/issues/{issue_number}"
    data = {
        "state": "closed"
    }
    data = json.dumps(data)
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    issue_result = requests.patch(url, data=data, headers=headers)
    issue_result = issue_result.json()


def github_create_branch(branch_name, repo_name, username, github_token):
    branches = github_get_all_branches(repo_name, username, github_token)

    if branch_name in branches:
        github_delete_branch(branch_name, repo_name, username, github_token)
    last_commit_sha = github_get_repo_sha(repo_name, username, github_token)
    url = f"https://api.github.com/repos/{username}/{repo_name}/git/refs"
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": last_commit_sha
    }
    data = json.dumps(data)
    headers = {"Authorization": f"Bearer {github_token}"}
    branch_result = requests.post(url, data=data, headers=headers)
    branch_result = branch_result.json()
    return branch_result.get("object", {}).get("sha")


def github_delete_branch(branch_name, repo_name, username, github_token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/{branch_name}"
    result = requests.delete(url, headers={"Authorization": f"Bearer {github_token}"})


def github_create_commit(last_commit_sha, repo_name, username, user_email, github_token, commit_content="yo", commit_message="yo"):
    blob_sha = github_create_commit_blob(repo_name, username, github_token, commit_content)
    tree_sha = github_create_commit_tree(blob_sha, last_commit_sha, repo_name, username, github_token)
    commit_sha = github_commit_tree(tree_sha, last_commit_sha, commit_message, repo_name, username, github_token)
    update_commit_ref(commit_sha, "pair-extraordinaire", repo_name, username, github_token)


def update_commit_ref(commit_sha, branch_name, repo_name, username, github_token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/{branch_name}"
    data = {
        "sha": commit_sha,
        "ref": f"refs/heads/{branch_name}"
    }
    data = json.dumps(data)
    result = requests.post(url, data=data, headers={"Authorization": f"Bearer {github_token}"})
    result = result.json()


def github_commit_tree(tree_sha, last_commit_sha, message, repo_name, username, github_token):
    commit_tree = {
        "message": message,
        "tree": tree_sha,
        "parents": [
            last_commit_sha
        ]
    }
    commit_tree = json.dumps(commit_tree)
    commit_tree_url = f"https://api.github.com/repos/{username}/{repo_name}/git/commits"
    commit_tree_result = requests.post(commit_tree_url, data=commit_tree, headers={"Authorization": f"Bearer {github_token}"})
    commit_tree_result = commit_tree_result.json()
    commit_tree_sha = commit_tree_result["sha"]
    return commit_tree_sha


def github_create_commit_tree(blob_sha, last_commit_sha, repo_name, username, github_token):
    commit_tree = {
        "base_tree": last_commit_sha,
        "tree": [
            {
                "path": "README.md",
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha
            }
        ]
    }
    commit_tree = json.dumps(commit_tree)
    commit_tree_url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees"
    commit_tree_result = requests.post(commit_tree_url, data=commit_tree, headers={"Authorization": f"Bearer {github_token}"})
    commit_tree_result = commit_tree_result.json()
    commit_tree_sha = commit_tree_result["sha"]
    return commit_tree_sha


def github_create_commit_blob(repo_name, username, github_token, blob_content="blob content"):
    bytes_blob = bytes(blob_content, "utf-8")
    base64_blob = base64.b64encode(bytes_blob).decode("utf-8")
    create_blob_url = f"https://api.github.com/repos/{username}/{repo_name}/git/blobs"
    data = {
        "content": base64_blob,
        "encoding": "base64"
    }
    data = json.dumps(data)
    blob = requests.post(create_blob_url, data=data, headers={"Authorization": f"Bearer {github_token}"})
    blob = blob.json()
    blob_sha = blob["sha"]
    return blob_sha


def github_get_repo_sha(repo_name, username, github_token):
    sha_url = f"https://api.github.com/repos/{username}/{repo_name}/git/refs/heads"
    sha = requests.get(sha_url, headers={"Authorization": f"Bearer {github_token}"})
    sha = sha.json()
    sha = sha[0]["object"]["sha"]
    return sha


def github_create_pull_request(title, body, head, repo_name, username, github_token):
    branches = github_get_all_branches(repo_name, username, github_token)
    branch_name = branches[0]["name"]
    for branch in branches:
        if branch["name"] == "main" or branch["name"] == "master":
            branch_name = branch["name"]
            break
    url = f"https://api.github.com/repos/{username}/{repo_name}/pulls"
    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": branch_name
    }
    result = requests.post(url, data=json.dumps(data), headers={"Authorization": f"Bearer {github_token}"})
    result = result.json()
    return result.get("number")


def github_get_all_branches(repo_name, username, github_token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/branches"
    branches = requests.get(url, headers={"Authorization": f"Bearer {github_token}"})
    branches = branches.json()
    return branches


def github_merge_pull_request(pull_request_number, title, message, repo_name, username, github_token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/pulls/{pull_request_number}/merge"
    data = {
        "commit_title": title,
        "commit_message": message,
    }
    result = requests.put(url, data=json.dumps(data), headers={"Authorization": f"Bearer {github_token}"})
    result = result.json()
    return result.get("sha")


def get_user_repos(github_token, fake_committer):
    url = f'https://api.github.com/users/{fake_committer}/repos'
    response = requests.get(url, headers={'Authorization': f'Bearer {github_token}'})
    return response.json()


def get_commit_by_repo(github_token, repo, fake_committer):
    url = f'https://api.github.com/repos/{fake_committer}/{repo}/commits'
    response = requests.get(url, headers={'Authorization': f'Bearer {github_token}'}, params={'author': fake_committer})
    return response.json()


def get_committer_creds(github_token, repo_name, fake_committer):
    if not repo_name:
        return False, False
    commits = get_commit_by_repo(github_token, repo_name, fake_committer)
    for commit in commits:
        c = (commit.get('commit'))
        cc = (commit.get('commit').get('committer'))
        return commit.get('commit', {}).get('committer', {}).get('name'), commit.get('commit', {}).get('committer', {}).get('email')
    return False, False


def get_user_email(github_token, fake_commiter):
    repos = get_user_repos(github_token, fake_commiter)
    for repo in repos:
        repo_name = repo.get('name')
        username, email = get_committer_creds(github_token, repo_name, fake_commiter)
        if not username or not email:
            continue
        if not username == fake_commiter:
            continue
        return email


def github_add_fake_commits_to_repository(github_token, git_repository_name, github_user_email, git_repository_owner, start_date, end_date):
    with tempfile.TemporaryDirectory() as temp_dir_path:
        environment_variables = {'GIT_TERMINAL_PROMPT': '0'}
        execute_command(['git', 'clone', f'https://{git_repository_owner}:{github_token}@github.com/{git_repository_owner}/{git_repository_name}', '.'], working_directory=temp_dir_path, environment_variables=environment_variables)
        execute_command(['git', 'config', 'user.name', git_repository_owner], working_directory=temp_dir_path, environment_variables=environment_variables)
        execute_command(['git', 'config', 'user.email', github_user_email], working_directory=temp_dir_path, environment_variables=environment_variables)

        while start_date <= end_date:
            date = start_date.strftime("%Y-%m-%d 11:11:22 +0200")
            os.environ['GIT_AUTHOR_DATE'] = date
            os.environ['GIT_COMMITTER_DATE'] = date
            start_date = start_date + datetime.timedelta(days=1)
            path = os.path.join(temp_dir_path, "try.txt")
            with open(path, "a+") as f:
                f.write("try")
            execute_command(['git', 'add', '.'], working_directory=temp_dir_path, environment_variables=environment_variables)
            execute_command(['git', 'commit', '-m', "try"], working_directory=temp_dir_path, environment_variables=environment_variables)

        execute_command(['git', 'push'], working_directory=temp_dir_path, environment_variables=environment_variables)


def github_add_contributors_to_repository(github_token, git_repository_owner, git_repository_name, contributors):
    with tempfile.TemporaryDirectory() as temp_dir_path:
        environment_variables = {'GIT_TERMINAL_PROMPT': '0'}
        execute_command(['git', 'clone', f'https://{git_repository_owner}:{github_token}@github.com/{git_repository_owner}/{git_repository_name}', '.'], working_directory=temp_dir_path, environment_variables=environment_variables)
        for contributor in contributors:
            username = contributor["username"]
            print(f"{username} is contributing!")
            email = contributor.get("email")
            if not email:
                email = get_user_email(github_token, username)
            if email is None:
                continue
            stdout, stderr, exit_code = execute_command(['git', 'config', 'user.name', username], working_directory=temp_dir_path, environment_variables=environment_variables)
            stdout, stderr, exit_code = execute_command(['git', 'config', 'user.email', email], working_directory=temp_dir_path, environment_variables=environment_variables)
            path = os.path.join(temp_dir_path, "try.txt")
            with open(path, "a+") as f:
                f.write("try")
            execute_command(['git', 'add', '.'], working_directory=temp_dir_path, environment_variables=environment_variables)
            execute_command(['git', 'commit', '-m', "try"], working_directory=temp_dir_path, environment_variables=environment_variables)
            execute_command(['git', 'push'], working_directory=temp_dir_path, environment_variables=environment_variables)


def github_remove_repository(github_token, git_repository_owner, git_repository_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {github_token}'
    }
    url = f"https://api.github.com/repos/{git_repository_owner}/{git_repository_name}"
    r = requests.delete(url, headers=headers)
    r.raise_for_status()


def github_create_repository(github_token, git_repository_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {github_token}'
    }
    url = r"https://api.github.com/user/repos"
    payload = {
        "name": git_repository_name,
        "auto_init": True
    }
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()


def github_get_username_from_token(github_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {github_token}'
    }
    url = r"https://api.github.com/user"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    json = r.json()
    return json['login']


def github_get_email_from_token(github_token):
    headers = {
        'Content-Type': 'application/json',
        "Accept": "application/vnd.github.v3+json",
        'Authorization': f'token {github_token}'
    }
    url = r"https://api.github.com/user/emails"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    json = r.json()
    for email_section in json:
        if email_section['primary']:
            email = email_section['email']
            return email


def fake_readme(github_token, github_username, profession, workplace):
    delete_repo(github_token, github_username, github_username)
    readme_content = f"""
# 👋 Hi there , I'm {github_username} 👋

I'm a **{profession}** at **@[{workplace}]({workplace}.com)** and i love *open source!*
![stats](https://user-images.githubusercontent.com/58976716/233138769-022c7589-c06d-4760-b691-546b29e30c51.svg)

### Current Projects
![img](https://user-images.githubusercontent.com/58976716/233132079-e85658cd-72f5-4d0c-8551-576bc7490fc1.svg)
![](https://user-images.githubusercontent.com/58976716/233132091-e12c1ae5-aa2d-4d96-a322-53728c03dc1b.svg)
![](https://user-images.githubusercontent.com/58976716/233132101-731619e9-9c72-41b2-90b5-1a54d799c84b.svg)
![](https://user-images.githubusercontent.com/58976716/233132113-ed445f9f-f477-47cf-ae4b-400fe836ac2a.svg)
"""
    readme_content = base64.b64encode(readme_content.encode('utf-8')).decode('utf-8')

    res = commit_file_to_repository(github_token, github_username, "README.md", readme_content)
    print(f"created readme for {github_username} at https://github.com/{github_username}/{github_username}\ncommit at {res['data']['createCommitOnBranch']['commit']['url']}")


def clean_readme(github_token, github_username):
    if os.path.exists(os.path.join(SCRIPT_DIR, github_username)):
        shutil.rmtree(os.path.join(SCRIPT_DIR, github_username))


def commit_file_to_repository(github_token, git_repository_name, file_name, file_content):
    url = "https://api.github.com/graphql"
    headers = {
        'Authorization': f'Bearer {github_token}'
    }
    repo_exists = requests.get(f"https://api.github.com/repos/{git_repository_name}/{git_repository_name}", headers=headers)
    if repo_exists.json().get("message") == "Not Found":
        github_create_repository(github_token, git_repository_name)

    commit_metadata_query = f"""
    {{
        repository(name: "{git_repository_name}", owner: "{git_repository_name}") {{
            defaultBranchRef {{
                target {{
                    ... on Commit {{
                    history(first: 1) {{
                    nodes {{
                        oid
                        }}
                        }}
                    }}
                }}
            }}
        }}
    }}
    """
    oid_query = requests.post(url, headers=headers, json={'query': commit_metadata_query})
    oid = oid_query.json()['data']['repository']['defaultBranchRef']['target']['history']['nodes'][0]['oid']

    query = """
    mutation ($input: CreateCommitOnBranchInput!) {
      createCommitOnBranch(input: $input) {
        commit {
          url
        }
      }
    }
    """

    variables = {
        "input": {
            "branch": {
                "repositoryNameWithOwner": f"{git_repository_name}/{git_repository_name}",
                "branchName": "main"
            },
            "message": {
                "headline": "totally real"
            },
            "fileChanges": {
                "additions": [
                    {
                        "path": file_name,
                        "contents": f"{file_content}"
                    }
                ],
            },
            "expectedHeadOid": oid
        }
    }

    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    response.raise_for_status()
    return response.json()


def delete_repo(github_token, user, repo):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    response = requests.delete(f'https://api.github.com/repos/{user}/{repo}', headers=headers)


def execute_command(command, raise_on_failure=True, working_directory=None, environment_variables=None, include_system_environment_variables=True):
    command_string = ' '.join(command)

    if environment_variables and include_system_environment_variables:
        temp_environment_variables = os.environ.copy()
        temp_environment_variables.update(environment_variables)
        environment_variables = temp_environment_variables

    process = subprocess.Popen(command, cwd=working_directory, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=environment_variables)
    stdout, stderr = process.communicate()

    if isinstance(stderr, bytes):
        stderr = stderr.decode()

    if isinstance(stdout, bytes):
        stdout = stdout.decode()

    exit_code = process.wait()
    if raise_on_failure and exit_code != 0:
        raise Exception(f'error executing command="{command_string}" exit code="{exit_code}" stderr="{stderr}" stdout="{stdout}"')

    return stdout, stderr, exit_code