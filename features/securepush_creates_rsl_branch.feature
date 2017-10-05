Feature: Secure-push creates an RSL branch
  In order to start securely pushing and fetching
  As a developer
  I want to be secure-push to create a new RSL branch when one doesn't exist

  @securepush
  Scenario: Create RSL branch
    Given a local copy of the repo on the feature branch
    When I run git-secure-push
    Then the rsl branch should now exist

