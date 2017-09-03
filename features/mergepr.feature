Feature: Merge PR

	@wip
	Scenario: Merge and prune branch
		Given A local copy of the repo on the master branch
		And The repo has a feature PR that is ready to merge
		When I run the git-mergepr command targeting devel
		Then The PR should be merged
		And The merge commit should be signed
		And The PR's branch should be deleted from git

	Scenario: Merge and keep branch
		Given A local copy of the repo on the feature branch
		And The repo has a feature PR that is ready to merge
		When I run the git-mergepr --no-prune command targeting devel
		Then The PR should be merged
		And The merge commit should be signed
		And The PR's branch should still exist

	Scenario: Fail when requesting branch does not exist
		Given A local copy of the repo on the master branch
		And The repo has a feature PR that is ready to merge
		When I run the git-mergepr command with a requesting branch that does not exist
		Then The script should fail with exit code 4

	Scenario: Fail when there is a merge conflict
		Given A local copy of the repo on the feature branch
		And The repo has a feature PR that is ready to merge
		And There is a merge conflict
		When I run the git-mergepr command targeting devel
		Then The script should fail with exit code 4