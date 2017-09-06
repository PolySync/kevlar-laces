Feature: Replaces work-in-progress when done
  In order to not lose my place
  As a developer
  I want the scripts to save and restore my local changes and return me to where I was

  @merge
  @remove_temp_files
  Scenario: Return repo to original working state after running script
    Given a local copy of the repo on the master branch
    And The repo has a feature PR that is ready to merge
    And I have done some work on the repo
    When I run the git-mergepr command targeting devel
    Then The repo should be returned to the state it was in before I ran the script

  @promote
  @remove_temp_files
  Scenario: Return repo to original working state after running script
    Given a local copy of the repo on the master branch
    And The repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    And I have done some work on the repo
    When I run the git-promote command from the command line
    Then The repo should be returned to the state it was in before I ran the script

  @merge
  Scenario: Return repo to original branch after running script
    Given a local copy of the repo on the feature branch
    And The repo has a devel PR that is ready to merge
    When I run the git-mergepr command targeting master
    Then The repo should be returned to the feature branch when I am done

  @promote
  Scenario: Return repo to original branch after running script
    Given a local copy of the repo on the feature branch
    And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
    When I run the git-promote command from the command line
    Then The repo should be returned to the feature branch when I am done