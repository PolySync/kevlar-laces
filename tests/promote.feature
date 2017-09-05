Feature: Promote to master

	Scenario: Promote branch to master
		Given A local copy of the repo on the master branch
    And The repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
		When I run the git-promote command from the command line
		Then The tag should be merged
		And The master branch should be tagged with the semver of the promoted branch
		And The merge commit should be signed
