Feature: Promote to master
  In order to ease the release workflow,
  As a developer
  I want to promote specific build tags to be a release

  @promote
  Scenario: Promote branch to master
    Given a local copy of the repo on the master branch
    And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    When I run the git-promote command from the command line
    Then the tag should be merged
    And the master branch should be tagged with the semver of the promoted branch
    And the merge commit should be signed

  @promote
  Scenario: Release tag already exists on remote
    Given a local copy of the repo on the master branch
    And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    And the remote repo has a release tag 1.0.1
    When I run the git-promote command from the command line
    Then the tag should not be merged
    And the script should return 11

