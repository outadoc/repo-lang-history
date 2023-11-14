#!/usr/bin/env python3

"""
This program generates the history of the number of lines of code present for each language in a given repository.
"""

import argparse
import datetime
import os
import subprocess
import tempfile
from git import Repo

DATE_FORMAT = '%Y-%m-%d %H:%M:%S %z'


def checkout_commit(repo, commit_hash):
    """
    Checkout the given commit hash.

    Args:
        repo: The repository object.
        commit_hash: The commit hash to checkout.

    Returns:
        None.
    """
    repo.git.checkout(commit_hash)


def get_hash_history(repo, skip_interval, from_date):
    """
    Get the commit hashes for the repository's history.

    Args:
        repo: The repository object.
        skip_interval: The interval to skip.

    Returns:
        A list of commit hashes.
    """
    # Keep 1 commit out of skip_interval
    return [c.hexsha for c in repo.iter_commits(rev=None, reverse=True, after=from_date)][::skip_interval]


def analyse(repo):
    """
    Analyze the repository using GitHub Linguist.

    Args:
        repo: The repository object.

    Returns:
        The output of the GitHub Linguist command.
    """
    cmd = ['github-linguist']
    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=repo.working_tree_dir)
    return result.stdout.decode().split('\n')


def get_current_commit_date(repo):
    """
    Get the current commit date.

    Args:
        repo: The repository object.

    Returns:
        The commit date.
    """
    commit = repo.head.commit
    return commit.committed_datetime.strftime(DATE_FORMAT)


def create_parser():
    """
    Creates a parser for the command line arguments.

    Returns:
        An ArgumentParser object.
    """
    parser = argparse.ArgumentParser(
        description='Generate the history of the number of lines of code for each language in a given repository.')
    parser.add_argument('repo', metavar='REPO', type=str,
                        help='path to the repository')
    parser.add_argument('-s', '--skip-interval', metavar='SKIP_INTERVAL',
                        type=int, default=5, help='interval of commits to skip (default: 5)')
    parser.add_argument('-o', '--output-file', type=str,
                        default='langstats.csv', help='File to append CSV output to')
    return parser


def get_latest_commit_date_from_output(output_file):
    with open(output_file, 'r') as history:
        history = history.readlines()
        last_line = history[-1]

        if not last_line:
            print("No existing history, starting from scratch")
            return None
        else:
            from_date_str = last_line.split(';')[1]

            # Add one second because otherwise we will include this commit twice
            from_date = datetime.datetime.strptime(
                from_date_str, DATE_FORMAT) + datetime.timedelta(seconds=1)

            print(f"Starting from {from_date}")
            return from_date


def main():
    """
    Main function that drives the program.

    Args:
        args: argparse Namespace object containing command-line arguments.

    Returns:
        None.
    """
    parser = create_parser()
    args = parser.parse_args()

    output_file = args.output_file

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, 'repo')

        # Clone the repository
        repo = Repo.clone_from(args.repo, repo_path)
        repo.config_writer().set_value('advice', 'detachedHead', 'false').release()

        # Start from where we left off
        from_date = get_latest_commit_date_from_output(output_file)

        with open(output_file, 'a') as history:
            for commit_hash in get_hash_history(repo, args.skip_interval, from_date):
                checkout_commit(repo, commit_hash)

                # Ignore libs for every commit
                with open(os.path.join(repo.working_tree_dir, '.gitattributes'), 'a') as f:
                    f.write('/*/libs/** linguist-vendored\n')

                commit_date = get_current_commit_date(repo)

                # Execute analysis
                output = analyse(repo)
                stats = ';'.join(output)

                # Append to CSV
                history.write(f'{commit_hash};{commit_date};{stats}\n')
                history.flush()

                # Restore .gitattributes
                try:
                    repo.git.checkout('--', '.gitattributes')
                except:
                    pass


if __name__ == '__main__':
    main()
