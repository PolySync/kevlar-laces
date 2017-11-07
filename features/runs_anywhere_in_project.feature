Feature: Runs successfully from anywhere in git project tree
  In order to not lose my place
  As a developer
  I want the scripts to save and restore my working directory and return me to where I was

  @merge
  Scenario: Return repo to original directory after running script
    Given a local copy of the repo on the master branch
    And the repo has a feature PR that is ready to merge
    And the project contains subdirectory dir
    When I run the git-merge-pr command from the dir directory
    Then the script exits with status 0
    And the dir directory should exist when I am done
    And the repo should be returned to the master branch when I am done

  @promote
  Scenario: Return repo to original directory after running script
    Given a local copy of the repo on the master branch
    And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    And the project contains subdirectory dir
    When I run the git-promote command from the dir directory
    Then the script exits with status 0
    And the dir directory should exist when I am done
    And the repo should be returned to the master branch when I am done

  @securefetch
  @securepush
  @securepull
  Scenario Outline: Return repo to original directory after running script
    Given a local copy of the repo on the feature branch
    And the project contains subdirectory dir
    When I run <command> from the dir directory
    Then the script exits with status 0
    And the dir directory should exist when I am done
    And the repo should be returned to the feature branch when I am done
  Examples:
    | command          |
    | git secure-fetch |
    | git secure-pull  |
    | git secure-push  |
