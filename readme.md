# Suits You — Custom-fit metrics for the fashion-conscious software developer

We both know you are the best software developer out there. All you need
is a chance to prove it. The code in this repository provides you with
the means of doing exactly that. It pulls in a bunch of quantitative
metrics about your contributions to larger projects on GitHub and uses
a simple linear regression algorithm to find a custom-fit "Contribution
Score Metric" that makes you come out ahead of the curve.

### Do you have some examples?

Sure. Just head over to the [demo](demo/) folder. It contains some
graphs that might be taken to indicate that I am the kind of guy you
should definitely be giving a promotion to ;)

### Why "Contribution Score Metric"?

Honestly, I couldn't come up with a better name. Feel free to rename
it to whatever you fancy. You might want to make sure that the name is
somewhat vague, however, since it is rather unlikely that the resulting
graphs provide any actual insight. They should look nice, though.

### Disclaimer

Any actual insight provided by graphs created with these scripts is
purely by accident. The author assumes no liability for any conclusions
reached by trying to actually interpret them.

### What is this anyway?

This project started as an assignment for the "Software Engineering"
class taught by [Prof Stephen Barrett] at Trinity College Dublin in
Michaelmas Term 2019. Since I had quite some fun implementing my solution,
I decided to open-source the code and push it to GitHub.

[Prof Stephen Barrett]: https://www.scss.tcd.ie/Stephen.Barrett/

### What metrics do you use?

The metrics can be divided into those relating to issues (including
pull requests) and those relating to commits (commit messages and
patches). They consist mostly of rather primitive counts of either the
number of issues, commits etc. or of the number of words (both total
and unique) or lines contained therein. Additionally, I also decided to
calculate averaged values for most of these counts. A complete list of all
the metrics gathered from GitHub is saved as [metrics.csv](metrics.csv).
The main idea was to simply obtain enough distinct values, so that the
linear regression algorithm used for fitting a combined "Contribution
Score Metric" would get a chance to separate any specific user from the
rest of the crowd.

### Why didn't you search for any real insight?

Software metrics — especially graphs displaying them in some nice and
apparently objective way — are all over the place. While looking into
ways of generating my own graphs for a college project, however, I became
suspicious of the methods used to create them. GitHub is an excellent
source for obtaining lots of quantitative data about a software engineer's
work. In my opinion, however, the quantitative data obtained in this way
consists of rather uninformative counts, such as Lines of Code added or
deleted and similar stuff with equally questionable information content.
We all know that Lines of Code are a horrible indicator for a software
engineer's performance. The rest of the measures doesn't seem much
better either.
This old and well known problem is why I took a different approach.
Rather than devising some odd combination of metrics by hand and giving
it a name that suggests that it actually shows how well someone is doing,
I did the reverse. I supposed that I was doing pretty well — that's
what we all like to think of ourselves anyhow, right? — and asked my
computer to create some graphs that would confirm this supposition.

As far as insight is concerned, you could view this project as a proof of
concept solution, showing that metrics gathered from GitHub can actually
be used to prove pretty much anything you like. Take the graphs contained
in the [demo](demo) folder, for instance. I hardly did any work on
[Abricotine] and much less on [joeynmt] and [edit-distance-js], yet I
was able to create some graphs that might be taken to suggest otherwise.
In my humble opinion, this shows that one should be suspicious to trust
metrics too easily — such as simply based on the fact that someone has
created a nice graph by throwing together a bunch of uninformative counts.

Note: I actually did a few commits to [joeynmt] as part of a university
project once, but I specified my college email in most of them, so
GitHub wasn't able to attribute them correctly and I didn't bother to
add a workaround for that sort of problem to `datadump.py`.

[Abricotine]: https://github.com/brrd/Abricotine/
[joeynmt]: https://github.com/joeynmt/joeynmt/
[edit-distance-js]: https://github.com/schulzch/edit-distance-js/


## Usage

### Dependencies

- [PyYAML]; used in all scripts for parsing the configuration file
- [PyGithub]; used for GitHub API calls in `datadump.py`
- [scikit learn]; used for fitting the custom metric in `learn.py`
- [Altair] and [pandas]; used for creating visualisations in
  `visualize.py`

[PyYAML]: https://pyyaml.org/
[PyGithub]: https://github.com/PyGithub/PyGithub/
[scikit learn]: https://scikit-learn.org/
[Altair]: https://altair-viz.github.io/
[pandas]: https://pandas.pydata.org/

### Configuration

An example configuration file, which was used to create the graphs
in the [demo](demo) folder, is included in this repository as
[config.yaml.example](config.yaml.example). To adjust the configuration,
simply copy `config.yaml.example` to `config.yaml` and adjust the
values. The configurable options are the following:

- **token**: An [access token for GitHub]. If specified, this token is
  used to authenticate the `datadump.py` script that downloads relevant
  data through the GitHub API. The script also works if this setting
  is omitted. Specifying a token greatly increases the number of API
  requests GitHub will accept per hour, however, and is therefore
  recommended.
- **user**: The GitHub username of the developer who is supposed to look
  good in the resulting diagrams. This user doesn't have to be the same
  as the one who created the token.
- **repos**: A list of upstream repositories the specified user has
  contributed to. Data from all these repositories will be combined for
  fitting the custom metric with `learn.py` and individual graphs for each
  one will be created by `visualize.py`.
- **balance-datasets**: If this option is set to `True` (the default),
  datasets will be balanced in `learn.py`. This means that data from
  repositories with few contributors will be used more often in the
  training process, so that the machine learner uses equal amounts of data
  from each repository. If this option is set to `False`, the machine
  learning algorithm will put more weight on data from repositories
  that have more contributors. It is recommended to try both settings
  and choose the one that results in nicer graphs.

[access token for GitHub]: https://github.blog/2013-05-16-personal-api-tokens/

### Running the scripts

The code in this repository is split across four independent scripts
that perform the different parts needed to fit the custom metric and
create nice visualisations. The scripts are supposed to be executed
in order, since each of them depends on the output the previous one
has written to disc. An invocation of all the scripts could look like
this:

```bash
./datadump.py   # Get relevant data from GitHub and save to data/
./vectorize.py  # Combine data and create vector representation
./learn.py      # Fit a custom metric that suits the specified user
./visualize.py  # Create nice diagrams in graphs/
```

## License

The source code contained in this repository may be copied under
the terms of the [GNU Affero General Public License, version 3 or
later][AGPL]. A copy of this license is included in the repository
as [license.md](license.md).

[AGPL]: https://www.gnu.org/licenses/agpl-3.0.en.html
