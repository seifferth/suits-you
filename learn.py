#!/usr/bin/env python3

import sys
import yaml
import os
import json
import random
from sklearn.linear_model import Lasso

with open("config.yaml") as f:
    config = yaml.safe_load(f)

class CombinedDataset():
    def __init__(self):
        self.datasets = list()
        self.X = list()
        self.y = list()
        self.unique_X = list()
        self.unique_y = list()
    def add_vectors(self, X, y):
        self.datasets.append((X, y))
    def balance(self):
        common_length = max(map(len, [ X for X, y in self.datasets ]))
        self.X = list()
        self.y = list()
        for X, y in self.datasets:
            self.X.extend(X)
            self.y.extend(y)
            for _ in range(common_length - len(X)):
                i = random.randint(0, len(X)-1)
                self.X.append(X[i])
                self.y.append(y[i])
    def make_unique(self):
        self.unique_X = list()
        self.unique_y = list()
        for X, y in self.datasets:
            for i in range(len(X)):
                if X[i] not in self.unique_X or y[i] not in self.unique_y:
                    self.unique_X.append(X[i])
                    self.unique_y.append(y[i])

def get_vectors(repo: str):
    repo_dir = os.path.join("data", repo.replace("/", "_"))
    filename = os.path.join(repo_dir, "vectors_X.json")
    with open(filename) as f:
        X = json.load(f)
    filename = os.path.join(repo_dir, "vectors_y.json")
    with open(filename) as f:
        y = json.load(f)
    return (X, y)


if __name__ == "__main__":
    dataset = CombinedDataset()
    for repo in config["repos"]:
        X, y = get_vectors(repo)
        dataset.add_vectors(X, y)
    dataset.balance()

    learner = Lasso(positive=True)
    learner.fit(dataset.X, dataset.y)

    dataset.make_unique()
    score = learner.score(dataset.unique_X, dataset.unique_y)
    w = learner.coef_
    print("Picking up user with an accuracy of {}".format(score),
        file=sys.stderr)

    with open("data/translation.json") as f:
        translate = json.load(f)

    weights = dict()
    for key, value in translate.items():
        weights[key] = w[value]
    with open("data/weights.json", mode="w") as f:
        json.dump(weights, f, indent=2)
    print("Weights saved to file", file=sys.stderr)
