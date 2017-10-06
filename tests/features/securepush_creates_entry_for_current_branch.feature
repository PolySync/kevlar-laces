Feature: Secure-push creates a push entry
  In order to start securely pushing
  As a developer
  I want to be secure-push to create push entries on the RSL branch

  @securepush
  Scenario: Pushes current branch
    Given a local copy of the repo on the feature branch
    And I create a new feature2 branch
    When I run git-secure-push
    Then the feature2 branch should now exist

  @securepush
  Scenario Outline: Push entry for current branch on RSL branch
    Given a local copy of the repo on the feature branch
    And I create a new feature2 branch
    When I run <command>
    Then the latest RSL entry should be a push entry
    And the latest RSL entry should contain Branch:feature2
  Examples:
	| command                          |
	| git-secure-push                  |
	| git-secure-push HEAD             |
	| git-secure-push feature2         |
	| git-secure-push HEAD:feature2    |
	| git-secure-push feature:feature2 |

  @securepush
  Scenario Outline: Push entry for not-current branch on RSL branch
    Given a local copy of the repo on the feature branch
    And I create a new feature2 branch
    And I create a new feature3 branch
    When I run <command>
    Then the latest RSL entry should be a push entry
    And the latest RSL entry should contain Branch:feature2
  Examples:
	| command                           |
	| git-secure-push feature2          |
	| git-secure-push feature2:feature2 |

  @securepush
  Scenario: Fail when GPG signing key is not available
    Given a local copy of the repo on the feature branch
    And the GPG signing key is not available
    When I run git-secure-push
    Then the script should return 4
