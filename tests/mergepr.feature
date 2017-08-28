Feature: Merge PR

	Scenario: Merge and prune branch
		Given A local copy of the repo
		And The repo has a feature PR that is ready to merge
		When I run the git-mergepr command targeting devel
		Then The PR should be merged
		And The merge commit should be signed
		And The PR's branch should be deleted from git

	Scenario: Merge and keep branch
		Given A local copy of the repo
		And The repo has a feature PR that is ready to merge
		When I run the git-mergepr --no-prune command targeting devel
		Then The PR should be merged
		And The merge commit should be signed
		And The PR's branch should still exist
