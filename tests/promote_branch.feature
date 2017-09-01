Feature: Promote to master

	@promote
	Scenario: Promote branch to master
		Given The repo exists
		And The repo has a development branch ready to promote to master
		When I run the git-promote command from the command line
		Then The branch should be merged into master
		And The merge commit should be signed
		And the master branch should be tagged with the semver of the promoted branch
