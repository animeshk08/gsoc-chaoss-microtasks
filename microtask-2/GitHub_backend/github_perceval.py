#! /usr/bin/env python3

import argparse

from perceval.backends.core.github import (GitHub,
                                           CATEGORY_ISSUE,
                                           CATEGORY_PULL_REQUEST,
                                           CATEGORY_REPO)
import datetime
import dateutil
import json

# Optional API token argument
parser = argparse.ArgumentParser(
    description="Simple parser for GitHub issues and pull requests"
    )
parser.add_argument("-t", "--token",
                    '--nargs', nargs='?',
                    help="GitHub token")

# Positional repository argument
parser.add_argument("repository",
                    help="GitHub repository, as 'owner/repo'")

args = parser.parse_args()

(owner, repository) = args.repository.split('/')


github = GitHub(owner=owner, repository=repository, api_token=[args.token], sleep_for_rate=True)


# Printing Owner and Repository
print("Owner: ", owner)
print("Repository: ", repository)
print("Categories: ", GitHub.CATEGORIES)

# Range of date between which data is to be fetched
from_date = datetime.datetime(2020, 3, 8, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
to_date = datetime.datetime(2020, 3, 9, 0, 0, 0, tzinfo=dateutil.tz.tzutc())

# Fetch Issue data
issue_list_generator = github.fetch(category=CATEGORY_ISSUE, from_date=from_date,
                                    to_date=to_date, filter_classified=False)
issue_list = list(issue_list_generator)




with open("github_issue.json", "w") as file:
    for issues in issue_list:
        json.dump(issues, file)

issue = issue_list[0]
# Printing some features of the issue
print('*'*50)
print("ISSUE")

print('Category: ', issue['category'])
print("Issue Count: ", len(issue_list))
print('Title: ', issue['data']['title'])
print('Comments: ', issue['data']['comments'])
print('Search Fields:', issue['search_fields'])
print('Timestamp: ', issue['timestamp'])
print('Updated on: ', issue['updated_on'])
print('UUID: ', issue['uuid'])
print('*'*50)

# Fetch Pull Request data

pr_list_generator = github.fetch(category=CATEGORY_PULL_REQUEST, from_date=from_date,
                                 to_date=to_date, filter_classified=False)
pr_list = list(pr_list_generator)

with open("github_pr.json", "w") as file:
    for prs in pr_list:
        json.dump(prs, file)

pr = pr_list[0]
# Printing some features of the repository data
print("PULL REQUEST")

print('Category: ', pr['category'])
print("Pull Request Count: ", len(pr_list))
print('Title: ', pr['data']['title'])
print('Comments: ', pr['data']['comments'])
print('Search Fields:', pr['search_fields'])
print('Timestamp: ', pr['timestamp'])
print('Updated on: ', pr['updated_on'])
print('UUID: ', pr['uuid'])
print('*'*50)

# Fetch repository data

repo_list_generator = github.fetch(category=CATEGORY_REPO, from_date=from_date,
                                    to_date=to_date, filter_classified=False)
repo_list = list(repo_list_generator)
print("Number: ", len(repo_list))

for repos in repo_list:
    with open("github_repo.json", "w") as file:
        json.dump(repos, file)

repo = repo_list[0]

# Printing some features of the repository data
print("REPOSITORY")

print('Category: ', repo['category'])
print("Repository Count: ", len(repo_list))
print('Description: ', repo['data']['description'])
print('Owner: ', repo['data']['owner']['login'])
# In case data is fetched from a repository item_id contains
# the timestamp when the data was fetched
print('Search Fields:', repo['search_fields'])
print('Timestamp: ', repo['timestamp'])
print('Updated on: ', repo['updated_on'])
print('UUID: ', repo['uuid'])
print('*'*50)

