#!/usr/bin/env python3

import sys
import github
import time
import yaml
import os

users = ["seifferth"]

if os.path.isfile("config.yaml"):
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
else:
    config = dict()

if "token" in config.keys():
    g = github.Github(login_or_token=config["token"])
else:
    g = github.Github()

def wait():
    """
    Check if rate limit is reached and wait if this is the case.
    """
    if g.get_rate_limit().core.remaining == 0:
        wait_time = g.rate_limiting_resettime - int(time.time())
        wait_time += 10 # Add 10 sec. just to be sure
        print("Reached rate limit. Waiting for {} mins.".format(
                round(wait_time/60)), file=sys.stderr)
        time.sleep(wait_time)

if __name__ == "__main__":
    for u in users:
        wait()
        u = g.get_user(login=u)
        wait()
        repos = u.get_repos()

        for r in repos:
            if r.fork:
                wait()  # Getting the parent's full name requires a request
                parent_name = r.parent.full_name
                print("{:<30} (forked from {})".format(r.name, parent_name))
            else:
                print(r.name)
