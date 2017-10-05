Feature: Easy to use command line interface with smart usage options and instructions.
In order to learn this tool quickly and easily
As a developer
I want to the scripts to have built in usage instructions

@merge @promote
Scenario Outline: Display usage and exit 0 when help flag is passed
  Given a local copy of the repo on the feature branch
  When the <command> command is run with the -h flag
  Then the terminal displays usage options for the <command> command
  And  the script exits with status 0

  Examples:
    | command |
    | merge-pr |
    | promote |

@merge
Scenario Outline: Parse options passed in any order
  Given a local copy of the repo on the feature branch
  And the repo has a feature PR that is ready to merge
  When I run the merge-pr command with the --no-prune option in position <position> targeting devel
  Then the PR should be merged
  And the feature branch should still exist

  Examples:
    | position |
    | 0        |
    | 1        |
    | 2        |

