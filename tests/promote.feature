Feature: Promote to master

	Scenario: Promote branch to master
		Given A local copy of the repo
		And The repo has a development branch ready to promote to master
		When I run the git-promote command from the command line
		Then The tag should be merged
		And The master branch should be tagged with the semver of the promoted branch
		And The merge commit should be signed
