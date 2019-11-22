#!/usr/bin/env python3

import sys
import github
import time
import yaml
import os
import json

if os.path.isfile("config.yaml"):
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
else:
    config = dict()

if "token" in config.keys():
    g = github.Github(login_or_token=config["token"])
    limit = 500     # Leave some requests for other programs
else:
    g = github.Github()
    limit = 0

def wait(verbose=False):
    """
    Check if rate limit is reached and wait if this is the case.
    """
    wait_time = g.rate_limiting_resettime - int(time.time())
    wait_time += 10 # Add 10 sec. just to be sure
    if g.get_rate_limit().core.remaining <= limit:
        print("Reached rate limit. Waiting for {} mins.".format(
                round(wait_time/60)), file=sys.stderr)
        time.sleep(wait_time)
    else:
        if verbose:
            print("{} requests left for the following {} mins.".format(
                g.get_rate_limit().core.remaining,
                round(wait_time/60),
                file=sys.stderr
            ))

def get_issues(r: github.Repository, data_dir: str):
    issues = dict()
    all_issues = r.get_issues(state="all")
    total = all_issues.totalCount
    cur = 0
    for i in all_issues:
        cur += 1
        if cur == 1 or cur%20 == 0:
            print("Processing issue {} of {}".format(cur, total),
                file=sys.stderr)
            wait(verbose=True)
        else:
            wait()
        login = i.user.login
        if login not in issues.keys():
            issues[login] = {
                                "num_issues": 0,
                                "open": 0,
                                "closed": 0,
                                "num_comments": 0,
                                "num_labels": 0,
                                "wordcount": 0,
                                "title_wordcount": 0,
                                "body_vocab": set(),
                                "body_vocab_filescope": 0,
                                "title_vocab": set(),
                                "title_vocab_filescope": 0,
                                "total_vocab_filescope": 0,
                            }
        data = issues[login]

        data["num_issues"] += 1
        if i.state == "open":
            data["open"] += 1
        elif i.state == "closed":
            data["closed"] += 1
        data["num_comments"] += i.get_comments().totalCount
        data["num_labels"] += len(i.labels)
        data["wordcount"] += len(i.body.split())
        data["title_wordcount"] += len(i.title.split())
        data["body_vocab"].update(set(i.body.split()))
        data["body_vocab_filescope"] += len(set(i.body.split()))
        data["title_vocab"].update(set(i.title.split()))
        data["title_vocab_filescope"] += len(set(i.title.split()))
        data["total_vocab_filescope"] += len(set(i.body.split()).union(
                                             set(i.title.split())))

    # Convert vocab sets to numbers
    for login in issues.keys():
        data = issues[login]
        data["total_vocab"] = len(data["body_vocab"].union(data["title_vocab"]))
        data["body_vocab"] = len(data["body_vocab"])
        data["title_vocab"] = len(data["title_vocab"])

    filename = os.path.join(data_dir, "issues.json")
    with open(filename+".part", mode="w") as f:
        json.dump(issues, f)
    os.rename(filename+".part", filename)

def get_commits(r: github.Repository, data_dir: str):
    commits = dict()
    all_commits = r.get_commits()
    total = all_commits.totalCount
    cur = 0
    for c in all_commits:
        cur += 1
        if cur == 1 or cur%10 == 0:
            print("Processing commit {} of {}".format(cur, total),
                file=sys.stderr)
            wait(verbose=True)
        else:
            wait()
        if c.author != None:
            login = c.author.login
        else:
            print("Skipping commit {} due to unknown author".format(c.sha),
                file=sys.stderr)
            continue
        if login not in commits.keys():
            commits[login] = {
                                "num_commits": 0,

                                "loc_additions": 0,
                                "loc_deletions": 0,
                                "loc_changes": 0,
                                "num_files": 0,

                                "loc_times_files": 0,
                                "loc_pow_files": 0,

                                "msg_wordcount": 0,
                                "msg_vocab": set(),
                                "msg_vocab_filescope": 0,
                                "patch_wordcount": 0,
                                "patch_vocab": set(),
                                "patch_vocab_filescope": 0,
                            }
        data = commits[login]

        data["num_commits"] += 1

        data["loc_additions"] += c.stats.additions
        data["loc_deletions"] += c.stats.deletions
        data["loc_changes"] += c.stats.total
        data["num_files"] += len(c.files)

        data["loc_times_files"] += c.stats.total * len(c.files)
        data["loc_pow_files"] += c.stats.total ** len(c.files)

        data["msg_wordcount"] += len(c.commit.message.split())
        data["msg_vocab"].update(set(c.commit.message.split()))
        data["msg_vocab_filescope"] += len(set(c.commit.message.split()))
        for f in c.files:
            if f.patch != None:
                data["patch_wordcount"] += len(f.patch.split())
                data["patch_vocab"].update(set(f.patch.split()))
                data["patch_vocab_filescope"] += len(set(f.patch.split()))

    # Convert vocab sets to numbers
    for login in commits.keys():
        commits[login]["msg_vocab"] = len(commits[login]["msg_vocab"])
        commits[login]["patch_vocab"] = len(commits[login]["patch_vocab"])

    filename = os.path.join(data_dir, "commits.json")
    with open(filename+".part", mode="w") as f:
        json.dump(commits, f)
    os.rename(filename+".part", filename)

if __name__ == "__main__":
    for x in config["repos"]:
        print("Processing {}".format(x), file=sys.stderr)
        data_dir = os.path.join("data", x.replace("/","_"))
        os.makedirs(data_dir, exist_ok=True)
        r = g.get_user(x.split("/")[0]).get_repo(x.split("/")[1])

        if os.path.isfile(os.path.join(data_dir, "issues.json")):
            print("Skipping issues due to existing data",
                file=sys.stderr)
        else:
            get_issues(r, data_dir=data_dir)
        if os.path.isfile(os.path.join(data_dir, "commits.json")):
            print("Skipping commits due to existing data",
                file=sys.stderr)
        else:
            get_commits(r, data_dir=data_dir)
