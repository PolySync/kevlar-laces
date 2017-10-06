Feature: --no-prune keeps feature branch
  In order to keep work on a long-lived feature branch even though I know it's a bad idea
  As a developer
  I want to be able to retain a branch even after its pull request is merged

  @merge
  Scenario: Merge and keep branch
    Given a local copy of the repo on the feature branch
    And the repo has a feature PR that is ready to merge
    When I run the git-merge-pr --no-prune command targeting devel
    Then the PR should be merged
    And the merge commit should be signed
    And the feature branch should still exist

