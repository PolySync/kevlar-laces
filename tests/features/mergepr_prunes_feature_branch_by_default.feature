Feature: prunes feature branch by default
  In order to keep things tidy
  As a developer
  I want to delete a feature branch after its pull request is merged

  @merge
  Scenario: Merge and prune branch
    Given a local copy of the repo on the master branch
    And the repo has a feature PR that is ready to merge
    When I run the git-merge-pr command targeting devel
    Then the PR should be merged
    And the merge commit should be signed
    And the feature branch should not exist

  @merge
  Scenario: Prevent running when feature branch is checked out locally
    Given a local copy of the repo on the feature branch
    And the repo has a feature PR that is ready to merge
    When I run the git-merge-pr command targeting devel
    Then the terminal prints an error
    And the script should return 10
    And the feature branch should still exist
