Feature: Secure-push creates a push entry
  In order to start securely pushing
  As a developer
  I want to be secure-push to create push entries on the RSL branch

  @securepush
  Scenario: Pushes current branch
    Given A local copy of the repo on the feature branch
    And I create a new feature2 branch
    When I run git-secure-push
    Then The feature2 branch should now exist

  @securepush
  Scenario: Push entry for current branch on RSL branch
    Given A local copy of the repo on the feature branch
    And I create a new feature2 branch
    When I run git-secure-push
    Then The latest RSL entry should be a push entry
    And The latest RSL entry should contain Branch:feature2

  @securepush
  Scenario: Push entry for not-current branch on RSL branch
    Given A local copy of the repo on the feature branch
    And I create a new feature2 branch
    And I create a new feature3 branch
    When I run git-secure-push feature2
    Then The latest RSL entry should be a push entry
    And The latest RSL entry should contain Branch:feature2

  @securepush
  Scenario: Fail when GPG signing key is not available
    Given A local copy of the repo on the feature branch
    And The GPG signing key is not available
    When I run git-secure-push
    Then The script should return 4
