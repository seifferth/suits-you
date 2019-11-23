#!/usr/bin/env python3

import sys
import yaml
import os
import json

if os.path.isfile("config.yaml"):
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
else:
    config = dict()

def get_empty_metric() -> dict:
        return {
                    ##################################
                    ##  Issues                      ##
                    ##################################

                    # Raw counts
                    "num_issues": 0,
                    "open": 0,
                    "closed": 0,
                    "num_comments": 0,
                    "num_labels": 0,
                    "wordcount": 0,
                    "title_wordcount": 0,
                    "body_vocab": 0,
                    "body_vocab_filescope": 0,
                    "title_vocab": 0,
                    "title_vocab_filescope": 0,
                    "total_vocab": 0,
                    "total_vocab_filescope": 0,
                    # Averaged counts
                    "avg_open": 0,
                    "avg_closed": 0,
                    "avg_num_comments": 0,
                    "avg_num_labels": 0,
                    "avg_wordcount": 0,
                    "avg_title_wordcount": 0,
                    "avg_body_vocab": 0,
                    "avg_title_vocab": 0,
                    "avg_total_vocab": 0,


                    ##################################
                    ##  Commits                     ##
                    ##################################

                    # Raw counts
                    "num_commits": 0,
                    "loc_additions": 0,
                    "loc_deletions": 0,
                    "loc_changes": 0,
                    "num_files": 0,
                    "loc_times_files": 0,
                    "loc_pow_files": 0,
                    "msg_wordcount": 0,
                    "msg_vocab": 0,
                    "msg_vocab_filescope": 0,
                    "patch_wordcount": 0,
                    "patch_vocab": 0,
                    "patch_vocab_filescope": 0,
                    # Averaged counts
                    "avg_loc_additions": 0,
                    "avg_loc_deletions": 0,
                    "avg_loc_changes": 0,
                    "avg_num_files": 0,
                    "avg_loc_times_files": 0,
                    "avg_loc_pow_files": 0,
                    "avg_msg_wordcount": 0,
                    "avg_msg_vocab": 0,
                    "avg_patch_wordcount": 0,
                    "avg_patch_vocab": 0,
               }

###################################################
##  Create translation dicst from empty metrics  ##
###################################################
index = { key: i for i, key in enumerate(get_empty_metric().keys()) }
unindex = dict()
for key, val in index.items():
    unindex[val] = key

def combine_metrics(issues: dict, commits: dict) -> dict:
    result = dict()
    usernames = set(issues.keys()).union(set(commits.keys()))
    for x in usernames:
        result[x] = get_empty_metric()
        data = result[x]

        # Copy any existing metrics
        if x in issues.keys():
            for key, value in issues[x].items():
                data[key] = value
        if x in commits.keys():
            for key, value in commits[x].items():
                data[key] = value

        # Calculate averages for issues:
        if data["num_issues"] != 0:
            data["avg_open"] = \
                    data["open"] / data["num_issues"]
            data["avg_closed"] = \
                    data["closed"] / data["num_issues"]
            data["avg_num_comments"] = \
                    data["num_comments"] / data["num_issues"]
            data["avg_num_labels"] = \
                    data["num_labels"] / data["num_issues"]
            data["avg_wordcount"] = \
                    data["wordcount"] / data["num_issues"]
            data["avg_title_wordcount"] = \
                    data["title_wordcount"] / data["num_issues"]
            data["avg_body_vocab"] = \
                    data["body_vocab_filescope"] / data["num_issues"]
            data["avg_title_vocab"] = \
                    data["title_vocab_filescope"] / data["num_issues"]
            data["avg_total_vocab"] = \
                    data["total_vocab_filescope"] / data["num_issues"]

        # Calculate averages for commits:
        if data["num_commits"] != 0:
            data["avg_loc_additions"] = \
                    data["loc_additions"] / data["num_commits"]
            data["avg_loc_deletions"] = \
                    data["loc_deletions"] / data["num_commits"]
            data["avg_loc_changes"] = \
                    data["loc_changes"] / data["num_commits"]
            data["avg_num_files"] = \
                    data["num_files"] / data["num_commits"]
            data["avg_loc_times_files"] = \
                    data["loc_times_files"] / data["num_commits"]
            data["avg_loc_pow_files"] = \
                    data["loc_pow_files"] / data["num_commits"]
            data["avg_msg_wordcount"] = \
                    data["msg_wordcount"] / data["num_commits"]
            data["avg_msg_vocab"] = \
                    data["msg_vocab_filescope"] / data["num_commits"]
            data["avg_patch_wordcount"] = \
                    data["patch_wordcount"] / data["num_commits"]
            data["avg_patch_vocab"] = \
                    data["patch_vocab_filescope"] / data["num_commits"]

    return result

def vectorize(metrics: dict):
    # Label user as 100 %
    user = config["user"]
    v_user = list()
    for i in range(len(unindex)):
        v_user.append(metrics[user][unindex[i]])
    del metrics[user]

    # Label everyone else as 0 %
    X = list(); y = list()
    for m in metrics.values():
        v = list()
        for i in range(len(unindex)):
            v.append(m[unindex[i]])
        X.append(v); y.append(0)
        X.append(v_user); y.append(1)

    return (X, y)

if __name__ == "__main__":
    for x in config["repos"]:
        print("Processing {}".format(x), file=sys.stderr)
        data_dir = os.path.join("data", x.replace("/","_"))
        issues_path = os.path.join(data_dir, "issues.json")
        commits_path = os.path.join(data_dir, "commits.json")

        if not os.path.isdir(data_dir) or not os.path.isfile(issues_path) \
                                       or not os.path.isfile(commits_path):
            print("No data found! Please run datadump.py first.",
                file=sys.stderr)
            exit(1)

        with open(issues_path) as f:
            issues = json.load(f)
        with open(commits_path) as f:
            commits = json.load(f)

        metrics_path = os.path.join(data_dir, "metrics")
        metrics = combine_metrics(issues=issues, commits=commits)
        with open(metrics_path+".json", mode="w") as f:
            json.dump(metrics, f, indent=2)

        vectors_path = os.path.join(data_dir, "vectors_{}.json")
        X, y = vectorize(metrics)
        with open(vectors_path.format("X"), mode="w") as f:
            json.dump(X, f)
        with open(vectors_path.format("y"), mode="w") as f:
            json.dump(y, f)

    translation_path = os.path.join("data", "translation.json")
    with open(translation_path, mode="w") as f:
        json.dump(index, f, indent=2)
