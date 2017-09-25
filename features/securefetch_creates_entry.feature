Feature: Secure-fetch create a fetch entry
  In order to start securely fetch
  As a developer
  I want to be secure-fetch or secure-pull to create fetch nonce entries on the RSL branch

  @securefetch
  Scenario Outline: Fetch entry for current branch on RSL branch
    Given A local copy of the repo on the feature branch
    And I create a new feature2 branch
    When I run <command>
    Then The latest RSL entry should be a fetch entry
  Examples:
	| command      |
    | git-secure-fetch |
	| git-secure-pull  |

  @securepush
  Scenario Outline: Fail when GPG signing key is not available
    Given A local copy of the repo on the feature branch
    And I create a new feature2 branch
    And The GPG signing key is not available
    When I run <command>
    Then The script should return 4
  Examples:
	| command      |
    | git-secure-fetch |
	| git-secure-pull  |
