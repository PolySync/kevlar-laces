# kevlar-laces

## Overview

kevlar-laces builds on git-rsl, adding the `git promote` and `git merge-pr` to
support PolySync's own development workflow on top of `secure-fetch` and
`secure-push`.

## Getting Started

### Dependencies

You'll need rust, and git. If you can build `git-rsl`, you should be able to
build this. 
* [rust](https://github.com/rust-lang-nursery/rustup.rs) (nightly)
* [git](https://git-scm.com/)
* [git-rsl](https://github.com/polysync/git-rsl)

### Building

Build with cargo.

* Build `kevlar-laces`
  ```bash
  cargo build
  ```

### Installation

`git-rsl` is not technically required to use this tool, but you'll
certainly be using it if you're using this.

* Install kevlar-laces
  ```bash
  cargo install
  ```

* Install git-rsl
  ```bash
  git clone git@github.com:PolySync/git-rsl.git
  cd git-rsl 
  cargo install
  ```

## Usage

`kevlar-laces` installs two new git subcommands, `git merge-pr` and `git promote`

```
git-merge-pr --help

git merge-pr 0.1.0
Rusell Mull <rmull@polysync.io>

USAGE:
    git-merge-pr [FLAGS] <src> <dest>

FLAGS:
    -h, --help        Prints help information
        --no-prune    Keep a local copy of the branch to be merged
    -V, --version     Prints version information

ARGS:
    <src>     The branch to merge
    <dest>    The destination branch


git-promote --help


/// TODO

```

### Examples

Suppose you have a product with a devel branch, off which feature branches are
created, and a master branch, representing the released software.

* Set up an example project
  ```bash
  mkdir sample-origin.git
  cd sample-origin.git
  git init . --bare
  cd ..
  
  git clone sample-origin.git sample-workspace
  cd sample-workspace
  
  git commit -m "Initial Revision"
  git secure-push origin master
  
  git co -b devel
  git secure-push origin devel
  ```
  
* Make a sample feature branch / pull-request
  ```bash
  cd sample-workspace
  git checkout -b feature-1
  echo "hello" > foo
  git add foo
  git commit -m "Change for feature-1"
  git secure-push origin feature-1
  ```
  
* Merge a pull request
  ```bash
  cd sample-workspace
  git checkout devel
  git merge-pr feature-1 devel
  ```

## Tests

There are some integration tests which set up some example repo structures and
run through some use cases.

### Building

Use cargo.

```bash
cargo build --tests
```

### Running

Automated tests are run with:

```bash
cargo test
```


# License

© 2018, PolySync Technologies, Inc.

* Russell Mull [rmull@polysync.io](mailto:rmull@polysync.io)

Please see the [LICENSE](./LICENSE) file for more details
