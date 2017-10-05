Feature: --no-prune keeps feature branch
  In order to keep work on a long-lived feature branch even though I know it's a bad idea
  As a developer
  I want to be able to retain a branch even after its pull request is merged

  @merge
  Scenario: Merge and keep branch
    Given A local copy of the repo on the feature branch
    And The repo has a feature PR that is ready to merge
    When I run the git-merge-pr --no-prune command targeting devel
    Then The PR should be merged
    And The merge commit should be signed
    And The feature branch should still exist

