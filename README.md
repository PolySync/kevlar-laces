# Kevlar Laces

## Overview

This project contains a collection of custom git subcommands to help the Engineering team more easily manage parts of the development and release workflows.

It is so-named as a homage to the idea of trying to provide some defense against a predictable cavalcade of typical foot-guns.

## Dependencies

This tool suite is intended to be exercised from git, so naturall git is a
prerequisite. Additionally, in order to sign commits and tags, you must also
have gpg2.

 * git
 * gnupg2

Running the tests will also require python, pip, and `behave`.

 * apt install python python-pip
 * pip install behave

## Installation

Clone the `kevlar-laces` repository to wherever you normally keep your
repositories. The install script will create symlinks to that location.
For example purposes, the `~/repos` directory is used, but any persistent
location will work.

```
$ cd ~/repos
$ git clone git@github.com:PolySync/kevlar-laces
$ cd kevlar-laces
$ . ./install.sh
```

The above example explicitly runs the install script with a preceding `.`. This
is solely for convenience in the _current_ terminal session, because
`install.sh` may need to modify `$PATH` to include `$HOME/.local/bin`. If you
already have `$HOME/.local/bin` in `$PATH` or you do not need to run the various
kevlar-laces git subcommands in the _current_ terminal session, then
`./install.sh` will suffice.


## Usage

### git-promote

When pull requests get merged into the `devel` development branch and Jenkins successfully builds it, then it will get auto-tagged with a semver version tag like `1.1.2-devel.54` when it's time to cut a release one of those tags will need to be promoted to the release branch.

The `promote` subcommand is intended to be used for promoting a development branch to release. For instance if your release branch was `master`, and your development branch tag was `1.1.2-devel.54`, then from inside the project repository you'd run:

```
git promote 1.1.2-devel.54 master
```

Which would do a signed merge of `devel` at `1.1.2-devel.54` into `master` and then tag `master` with `1.1.2`, thus creating the `1.1.2` release.

### git-merge-pr

The web UIs of GitHub and BitBucket don't create signed merge commits, which creates a problem when trying to measure the validity of a repository. So PRs need to be merged and pushed outside the web UIs.

The `merge-pr` subcommand is to help make it easier to merge PRs without interrupting your workflow when working on a project. If the branch requesting to be merged was `bugfix/fix-all-yo-bugz`, and the destination branch to merge to is `devel`, then from inside the project repository you'd run:

```
git merge-pr bugfix/fix-all-yo-bugz devel
```

This will result in any changes in your current working tree being stashed, the remote changes for the repo being fetched, the PR being merged, and your stashed changes being unstashed so you can keep working.

By default the `merge-pr` subcommand will also prune the requesting branch after it has been merged. If you want to disable this then call the command with the `--no-prune` flag like:

```
git merge-pr --no-prune bugfix/fix-all-yo-bugz devel
```

### git-secure-push

Git is vulnerable to metadata attacks as detailed in the [RSL paper](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_torres-arias.pdf).
In order to create a signed and replicated state log the `git-secure-push` and
`git-secure-fetch`/`git-secure-pull` commands work in concert to create a
reference state log for branches and tags that can be verified by other
developers to ensure the repository metadata is consistent (or at least the
parts known during the last interaction with the Bitbucket or GitHub server are
unchanged).

The `securepush` subcommand will only push the specified branch, or else the currently
checked out branch if none is specified. It will also prompt for GPG signatures
twice: first for the clearsign of the current metadata state for this branch,
and second for the commit containing that metadata.  The `secure-push` command
will also create the `rsl` branch if necessary.

```
git secure-push
git secure-push HEAD
git secure-push HEAD:remote_branch
git secure-push local_branch
git secure-push local_branch:remote_branch
```


### git-secure-fetch

Git is vulnerable to metadata attacks as detailed in the [RSL paper](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_torres-arias.pdf).
In order to create a signed and replicated state log the `git-secure-push` and
`git-secure-fetch`/`git-secure-pull` commands work in concert to create a
reference state log for branches and tags that can be verified by other
developers to ensure the repository metadata is consistent (or at least the
parts known during the last interaction with the Bitbucket or GitHub server are
unchanged).

The `secure-fetch` subcommand will only fetch the currently checked out branch. It
will also create a nonce on the `rsl` branch and therefore will prompt for GPG signature as part of that commit.

The `secure-fetch` subcommand will not merge any changes into the local working
branch. For that you'll either need to use `git merge` explicitly, or use `git
secure-pull`.

```
git secure-fetch
```

### git-secure-pull

Git is vulnerable to metadata attacks as detailed in the [RSL paper](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_torres-arias.pdf).
In order to create a signed and replicated state log the `git-secure-push` and
`git-secure-fetch`/`git-secure-pull` commands work in concert to create a
reference state log for branches and tags that can be verified by other
developers to ensure the repository metadata is consistent (or at least the
parts known during the last interaction with the Bitbucket or GitHub server are
unchanged).

The `secure-pull` subcommand will only fetch and merge the currently checked out branch. It
will also create a nonce on the `rsl` branch and therefore will prompt for GPG signature as part of that commit.

The `secure-pull` subcommand will only attempt to fast-forward merge any upstream
changes and will fail if it is unable to do so. If you need a recursive/3-way
merge, you'll need to explicitly use `git merge`.

```
git secure-pull
```



## Tests

The behavior for each of the tools are specified in [Gherkin](https://cucumber.io/docs/reference)
feature files. Each of the Given, When, Then steps for the feature files are
implemented in using [Behave](https://pythonhosted.org/behave/tutorial.html).

The features are laid out according to the expectations of users for this suite
of tools (like `features/unique_error_codes.feature` or
`features/replaces_work_in_progress.feature`) rather than a feature file for
each of the tools in the suite. This encourages a uniform feel across the tool
suite. Individual steps (Given, When, Then) should try to exercise commonality,
but are free to isolate their steps in their own implementation files.

### Installing Dependencies

In order to run the tests, you'll need behave, which in turn relies upon python.

```
$ apt install gnupg2 git python python-pip
$ pip install behave pyhamcrest

```

### Running Tests

The `Jenkinsfile` specifies how Jenkins will execute the tests; however, you may
(and probably should) run the tests locally using `behave`.

#### Running the entire test suite

```
$ behave
...
5 features passed, 0 failed, 0 skipped
11 scenarios passed, 0 failed, 0 skipped
55 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m6.477s

```

#### Running a specific feature test

```
$ behave features/unique_error_codes.feature
...
1 feature passed, 0 failed, 0 skipped
6 scenarios passed, 0 failed, 0 skipped
27 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.730s

```

#### Running the tests for a specific subcomponent

```
$ behave --tags promote -k
...
3 features passed, 0 failed, 2 skipped
5 scenarios passed, 0 failed, 6 skipped
25 steps passed, 0 failed, 30 skipped, 0 undefined
Took 0m2.592s

```


# License

FULLY CLOSED SOURCE LICENSE (FCSL)

Copyright (c) 2017 PolySync Technologies, Inc.

Don't copy or redistribute this Software until this license has been intentionally modified by someone with the authority and purview to do so (e.g. a person within PolySync with both technology organization ownership and legal signing authority).
Also, the above.
