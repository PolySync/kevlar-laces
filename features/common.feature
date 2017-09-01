Feature: Common to both scripts

	Scenario Outline: Fail when target branch does not exist
		Given a local copy of the repo on the master branch
    	And The repo has <what>
		When I run the <command> targeting a branch that does not exist
		Then the script should fail with exit code <exit_code>

		Examples:
		| what		| command		| exit_code |
		| prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1	| git-promote command | 3 |
		| a feature PR that is ready to merge |git-mergepr command | 3 |

	@remove_temp_files
	Scenario Outline: Return repo to original working state after running script
		Given a local copy of the repo on the master branch
    	And The repo has <what>
    	And I have done some work on the repo
    	When I run the <command>
    	Then The repo should be returned to the state it was in before I ran the script

    	Examples:
    	| what		| command		|
    	| prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1 | git-promote command from the command line |
    	| a feature PR that is ready to merge | git-mergepr command targeting devel |

    Scenario Outline: Fail when Yubikey not inserted
		Given a local copy of the repo on the master branch
		And The repo has <what>
		And My Yubikey is not inserted
		When I run the <command>
		Then the script should fail with exit code <exit_code>

		Examples:
		| what		| command		| exit_code |
		|prerelease tag 1.0.1-devel.3 to promote to master as 1.0.1 | git-promote command from the command line | 5 |
		| a feature PR that is ready to merge | git-mergepr command targeting devel | 4 |