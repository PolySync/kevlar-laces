Feature: Unique error codes for problematic situations
  In order to diagnose the exact cause when a problem occurs
  As a developer
  I want to have a unique exit code for each situation

  @merge
  Scenario: Fail when requesting branch does not exist
    Given A local copy of the repo on the master branch
    And The repo has a feature PR that is ready to merge
    When I run the git-mergepr command with a requesting branch that does not exist
    Then The script should return 4

  # @broken
  # Scenario: Fail when there is a merge conflict
  #   Given A local copy of the repo on the feature branch
  #   And The repo has a feature PR that is ready to merge
  #   And There is a merge conflict
  #   When I run the git-mergepr command targeting devel
  #   Then The script should return 4

  @merge
  Scenario: Fail when target branch does not exist
    Given a local copy of the repo on the master branch
    And The repo has a feature PR that is ready to merge
    When I run the git-mergepr command targeting a branch that does not exist
    Then the script should return 3

  @merge
  Scenario: Fail when Yubikey not inserted
    Given a local copy of the repo on the master branch
    And The repo has a feature PR that is ready to merge
    And My Yubikey is not inserted
    When I run the git-mergepr command targeting devel
    Then the script should return 4

  @promote
  Scenario: Fail when release tag already exists
    Given a local copy of the repo on the master branch
    And The repo has prerelease tag 1.0.0-devel.1 to promote to master as 1.0.0
    And The 1.0.0 release tag already exists
    When I run the git-promote command from the command line
    Then The script should return 6

  @promote
  Scenario: Fail when target branch does not exist
    Given a local copy of the repo on the master branch
    And The repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    When I run the git-promote command targeting a branch that does not exist
    Then the script should return 3

  @promote
  Scenario: Fail when Yubikey not inserted
    Given a local copy of the repo on the master branch
    And The repo has prerelease tag 1.0.1-devel.3 to promote to master as 1.0.1
    And My Yubikey is not inserted
    When I run the git-promote command from the command line
    Then the script should return 5

