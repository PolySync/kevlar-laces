# Git Kevlar Laces

## Overview

This project contains a collection of custom git subcommands to help the Engineering team more easily manage parts of the development and release workflows.

It is so-named as a homage to the idea of trying to provide some defense against a predictable cavalcade of typical foot-guns.

## Installation

Who knows... probably something to do with cloning the repo at a certain version into `~/.local/bin` or something like that.

## Usage

### git-promote

When pull requests get merged into the `devel` development branch and Jenkins successfully builds it, then it will get auto-tagged with a semver version tag like `1.1.2-devel.54` when it's time to cut a release one of those tags will need to be promoted to the release branch.

The `promote` subcommand is intended to be used for promoting a development branch to release. For instance if your release branch was `master`, and your development branch tag was `1.1.2-devel.54`, then from inside the project repository you'd run:

```
git promote 1.1.2-devel.54 master
```

Which would do a signed merge of `devel` at `1.1.2-devel.54` into `master` and then tag `master` with `1.1.2`, thus creating the `1.1.2` release.

### git-mergepr

The web UIs of GitHub and BitBucket don't create signed merge commits, which creates a problem when trying to measure the validity of a repository. So PRs need to be merged and pushed outside the web UIs.

The `mergepr` subcommand is to help make it easier to merge PRs without interrupting your workflow when working on a project. If the branch requesting to be merged was `bugfix/fix-all-yo-bugz`, and the destination branch to merge to is `devel`, then from inside the project repository you'd run:

```
git mergepr bugfix/fix-all-yo-bugz devel
```

This will result in any changes in your current working tree being stashed, the remote changes for the repo being fetched, the PR being merged, and your stashed changes being unstashed so you can keep working.

By default the `mergepr` subcommand will also prune the requesting branch after it has been merged. If you want to disable this then call the command with the `--no-prune` flag like:

```
git mergepr --no-prune bugfix/fix-all-yo-bugz devel
```

## Tests

### Installing Dependencies

### Running Tests

# License

FULLY CLOSED SOURCE LICENSE (FCSL)

Copyright (c) 2017 PolySync Technologies, Inc.

Don't copy or redistribute this Software until this license has been intentionally modified by someone with the authority and purview to do so (e.g. a person within PolySync with both technology organization ownership and legal signing authority).
Also, the above.
