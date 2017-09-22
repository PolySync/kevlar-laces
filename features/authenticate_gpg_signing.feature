Feature: Allow merging of unsigned commits
    In order to faciliate our current authentication methods,
    As a developer
    I want to allow signed merging of unsigned commits
    
    @merge
    Scenario: Merge PR with unsigned commits in log
        Given A local copy of the repo on the master branch
        And The repo has a feature PR that is ready to merge
        And The feature branch contains unsigned commits
        When I run the git-merge-pr command targeting devel
        Then The PR should be merged
        And The merge commit should be signed

    @promote
    Scenario: Promote unsigned tag to master
        Given A local copy of the repo on the feature branch
        And The repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
        And The 1.0.1-devel.2 tag is unsigned
        When I run the git-promote command from the command line
        Then The tag should be merged
        And The master branch should be tagged with the semver of the promoted branch
        And The merge commit should be signed

    @promote
    Scenario: Promote tag with unsigned commits to master
        Given A local copy of the repo on the feature branch
        And The repo has prerelease tag 1.0.1-devel.2 to promote to master as 1.0.1
        And The 1.0.1-devel.2 tag contains unsigned commits
        When I run the git-promote command from the command line
        Then The tag should be merged
        And The master branch should be tagged with the semver of the promoted branch
        And The merge commit should be signed
