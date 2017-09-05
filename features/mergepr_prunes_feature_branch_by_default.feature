Feature: prunes feature branch by default
  In order to keep things tidy
  As a developer
  I want to delete a feature branch after its pull request is merged

  @merge
  Scenario: Merge and prune branch
    Given A local copy of the repo on the master branch
    And The repo has a feature PR that is ready to merge
    When I run the git-mergepr command targeting devel
    Then The PR should be merged
    And The merge commit should be signed
    And The feature branch should not exist

