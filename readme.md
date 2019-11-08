# Measuring Engineering (Project) / Social Graph

This is a gitlab project for the michaelmas term class in Software
Engineering (CS3012/CSS33012) taught by Stephen Barrett.

## Dependencies

- [PyGithub](https://github.com/PyGithub/PyGithub)
  (`pip install --user PyGithub`)

## Configuration

An optional configuration file can be profided as `config.yaml`. At
the moment, this file can be used to specify a GitHub access token,
which will increase the rate limiting. A token may be included in
this way:

```yaml
token: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
