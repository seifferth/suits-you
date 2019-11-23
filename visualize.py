#!/usr/bin/env python3

import sys
import yaml
import os
import json
import altair
import pandas
import math

if os.path.isfile("config.yaml"):
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
else:
    config = dict()

def get_weights():
    with open(os.path.join("data", "weights.json")) as f:
        w = json.load(f)
    for key, val in w.items():
        if val <= 0:
            w[key] = 0
        else:
            w[key] = val
    print("\n".join([key for key, val in w.items() if val != 0]))
    return w

def save_graphs(repo, weights):
    repo_dirname = repo.replace("/", "_")
    metrics_path = os.path.join("data", repo_dirname, "metrics.json")
    with open(metrics_path) as f:
        metrics = json.load(f)
    logins = list(metrics.keys())
    logins.sort()

    data = { "user": logins, "score": list() }
    for u in logins:
        score = 0
        for key, val in metrics[u].items():
            score += weights[key] * val
        #data["score"].append(score)
        data["score"].append(math.log(score))

    sorting = list()
    for i in range(len(data["user"])):
        sorting.append((data["score"][i], data["user"][i]))
    sorting.sort()
    sorting = [ x[1] for x in sorting ]
    sorting.reverse()

    altair.Chart(pandas.DataFrame(data)).mark_bar().encode(
            x="score",
            y=altair.Y("user", sort=sorting),
        ).save(os.path.join("graphs", repo_dirname+".html"))


if __name__ == "__main__":
    weights = get_weights()
    os.makedirs("graphs", exist_ok=True)
    for repo in config["repos"]:
        save_graphs(repo, weights)
