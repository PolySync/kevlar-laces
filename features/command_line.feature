Feature: Easy to use command line interface with smart usage options and instructions.
In order to learn this tool quickly and easily
As a developer
I want to the scripts to have built in usage instructions

@merge @promote
Scenario Outline: Display usage and exit 0 when help flag is passed
  Given A local copy of the repo on the feature branch
  When The <command> command is run with the -h flag
  Then The terminal displays usage options for the <command> command
  And  The script exits with status 0

  Examples:
    | command |
    | merge-pr |
    | promote |

@merge
Scenario Outline: Parse options passed in any order
  Given A local copy of the repo on the feature branch
  And The repo has a feature PR that is ready to merge
  When I run the merge-pr command with the --no-prune option in position <position> targeting devel
  Then The PR should be merged
  And The feature branch should still exist

  Examples:
    | position |
    | 0        |
    | 1        |
    | 2        |

