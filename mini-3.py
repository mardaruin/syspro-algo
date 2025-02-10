import os
import subprocess


def run_command(command):
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.returncode == 0


def checkout_commit(commit_hash):
    subprocess.run(["git", "checkout", commit_hash], cwd=repo_path)


def get_commits_in_range(start_hash, end_hash):
    command = f'git log --pretty="%H" {start_hash}..{end_hash}'
    output = subprocess.check_output(command.split(), cwd=repo_path).decode('utf-8')
    return [commit.strip('\"') for commit in output.split('\n') if commit.strip()]


def binary_search(commits, check_command):
    low = 0
    high = len(commits) - 1

    while low <= high:
        mid = (low + high) // 2
        current_commit = commits[mid]

        checkout_commit(current_commit)

        if run_command(check_command):
            print(f"Good commit: {current_commit}")
            low = mid + 1
        else:
            print(f"Bad commit found: {current_commit}")
            high = mid - 1

    return commits[high]


if __name__ == "__main__":
    import sys

    repo_path = 'C:/Users/Marina Rudometova/PycharmProjects/syspro-algo/test_dir'
    start_hash = 'f348e1a1abfe7c3070f36bbab0b082f6154aacc5'
    end_hash = '7491fe702de4908fabf04bd74dadeea7028256a3'
    check_command = 'findstr /m bad a_file.txt'

    os.chdir(repo_path)

    commits = get_commits_in_range(start_hash, end_hash)

    bad_commit = binary_search(commits, check_command)

    print(f"The first bad commit is: {bad_commit}")
#the first bad commit must be 91b59392b31cf091708315f486d6ac3f067d783e