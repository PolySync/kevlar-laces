Feature: Unique error codes for problematic situations
  In order to diagnose the exact cause when a problem occurs
  As a developer
  I want to have a unique exit code for each situation

  @merge
  Scenario: Fail when the branch to be merged does not exist
    Given a local copy of the repo on the master branch
    And the repo has a feature PR that is ready to merge
    When I run the git-merge-pr command with a branch to be merged that does not exist
    Then the script should return 4

  @merge
  Scenario: Fail when there is a merge conflict
    Given a local copy of the repo on the master branch
    And the repo has a feature PR that is ready to merge
    And there is a merge conflict
    When I run the git-merge-pr command targeting devel
    Then the script should return 4

  @merge
  Scenario: Fail when target branch does not exist
    Given a local copy of the repo on the master branch
    And the repo has a feature PR that is ready to merge
    When I run the git-merge-pr command targeting not_a_branch
    Then the script should return 3

  @merge
  Scenario: Fail when GPG signing key is not available
    Given a local copy of the repo on the master branch
    And the repo has a feature PR that is ready to merge
    And the GPG signing key is not available
    When I run the git-merge-pr command targeting devel
    Then the script should return 2

  @merge
  Scenario: Fail when branch exists locally but not remotely
    Given a local copy of the repo on the devel branch
    And the repo has a feature PR that is ready to merge
    But the feature branch does not exist remotely
    When I run the git-merge-pr command targeting devel
    Then the script should return 4

  @merge
  Scenario: Fail branch when merge-pr called without --no-prune flag on feature branch
    Given a local copy of the repo on the feature branch
    And the repo has a feature PR that is ready to merge
    When I run the git-merge-pr command targeting devel
    Then the script should return 10

  @promote
  Scenario: Fail when release tag already exists
    Given a local copy of the repo on the master branch
    And the repo has prerelease tag 1.0.0-devel.1 to promote to master as 1.0.0
    And the 1.0.0 release tag already exists
    When I run the git-promote command from the command line
    Then the script should return 11

  @promote
  Scenario: Fail when target branch does not exist
    Given a local copy of the repo on the master branch
    And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    When I run the git-promote command targeting not_a_branch
    Then the script should return 3

  @promote
  Scenario: Fail when GPG signing key is not available
    Given a local copy of the repo on the master branch
    And the repo has prerelease tag 1.0.1-devel.3 to promote to master as 1.0.1
    And the GPG signing key is not available
    When I run the git-promote command from the command line
    Then the script should return 2

