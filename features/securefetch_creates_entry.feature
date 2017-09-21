Feature: Secure-fetch creates a fetch entry
  In order to start securely fetch
  As a developer
  I want to be secure-fetch to create fetch nonce entries on the RSL branch

  @securefetch
  Scenario: Fetch entry for current branch on RSL branch
    Given A local copy of the repo on the feature branch
    And I create a new feature2 branch
    When I run git-secure-fetch
    Then The latest RSL entry should be a fetch entry
