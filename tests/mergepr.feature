Feature: Merge PR

	Scenario: Merge and prune branch
		Given The repo exists
		And The repo has a PR that is ready to merge
		When I run the git-mergepr command from the command line
		Then The PR should be merged
		And The merge commit should be signed
		And The PR's branch should be deleted from git

	Scenario: Merge and keep branch
		Given The repo exists
		And The repo has a PR that is ready to merge
		When I run the git-mergepr --no-delete command from the command line
		Then The PR should be merged
		And The merge commit should be signed
		And The PR's branch should still exist
