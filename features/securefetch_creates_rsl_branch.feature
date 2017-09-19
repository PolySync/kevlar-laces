Feature: Securefetch creates an RSL branch
  In order to start securely pushing and fetching
  As a developer
  I want to be securefetch to create a new RSL branch when one doesn't exist

  @securefetch
  Scenario: Create RSL branch
    Given A local copy of the repo on the feature branch
    When I run git-securefetch
    Then The rsl branch should now exist

