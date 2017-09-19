Feature: Securepush creates an RSL branch
  In order to start securely pushing and fetching
  As a developer
  I want to be securepush to create a new RSL branch when one doesn't exist

  @securepush
  Scenario: Create RSL branch
    Given A local copy of the repo on the feature branch
    When I run git-securepush
    Then The rsl branch should now exist

