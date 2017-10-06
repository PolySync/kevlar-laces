Feature: Allow merging of unsigned commits
    In order to faciliate our current authentication methods,
    As a developer
    I want to allow signed merging of unsigned commits
    
    @merge
    Scenario: Merge PR with unsigned commits in log
        Given a local copy of the repo on the master branch
        And the repo has a feature PR that is ready to merge
        And the feature branch contains unsigned commits
        When I run the git-merge-pr command targeting devel
        Then the PR should be merged
        And the merge commit should be signed

    @promote
    Scenario: Promote unsigned tag to master
        Given a local copy of the repo on the feature branch
        And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
        And the 1.0.1-devel.2 tag is unsigned
        When I run the git-promote command from the command line
        Then the tag should be merged
        And the master branch should be tagged with the semver of the promoted branch
        And the merge commit should be signed

    @promote
    Scenario: Promote tag with unsigned commits to master
        Given a local copy of the repo on the feature branch
        And the repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
        And the 1.0.1-devel.2 tag contains unsigned commits
        When I run the git-promote command from the command line
        Then the tag should be merged
        And the master branch should be tagged with the semver of the promoted branch
        And the merge commit should be signed
