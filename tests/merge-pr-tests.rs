#[macro_use]
extern crate lazy_static;

extern crate assert_cli;
use assert_cli::{Assert, Environment};

extern crate tempfile;
extern crate git2;
extern crate git_rsl;

mod fixture;
use fixture::TestFixture;

use git_rsl::{BranchName, RemoteName};

use std::sync::Mutex;

lazy_static! {
    static ref SEQUENTIAL_TEST_MUTEX: Mutex<()> = Mutex::new(());
}

fn create_pr(e: &Environment, repo: &str, pr_name: &str) {
    // make a PR branch
    let bar_path = &format!("{}/bar", repo);
    fixture::runv(&e, &[
        &["git", "checkout", "-b", pr_name],
        &["touch", bar_path],
        &["git", "add", bar_path],
        &["git", "commit", "-m", "pr revision"]
    ]);

    let mut gr = git2::Repository::open(repo).unwrap();
    git_rsl::secure_push_with_cleanup(&mut gr,
                                      &RemoteName::new("origin"),
                                      &BranchName::new(pr_name))
        .unwrap();
}


#[test]
fn test_basic() {
    let _guard = SEQUENTIAL_TEST_MUTEX.lock();
    let fixture = TestFixture::new();

    create_pr(&fixture.env, fixture.local_path(), "test-pr");
    fixture::run(&fixture.env, &["git", "checkout", "master"]);

    // merge it
    Assert::cargo_binary("git-merge-pr")
        .with_env(&fixture.env)
        .with_args(&["test-pr", "master"])
        .stdout().contains("Pushing updated RSL to remote")
        .unwrap();

    // The test-pr branch should be gone now
    Assert::command(&["git", "branch", "--all"])
        .with_env(&fixture.env)
        .stdout().doesnt_contain("test-pr")
        .unwrap();
}


#[test]
fn test_no_prune() {
    let _guard = SEQUENTIAL_TEST_MUTEX.lock();
    let fixture = TestFixture::new();
    create_pr(&fixture.env, fixture.local_path(), "test-pr");

    // should print an error message when on the test-pr branch
    fixture::run(&fixture.env, &["git", "checkout", "test-pr"]);
    Assert::cargo_binary("git-merge-pr")
        .with_env(&fixture.env)
        .with_args(&["test-pr", "master"])
        .fails_with(2)
        .stdout().contains("You are checked out on the branch you are trying to merge")
        .unwrap();

   // But it should then work with no-prune
    Assert::cargo_binary("git-merge-pr")
        .with_env(&fixture.env)
        .with_args(&["test-pr", "master", "--no-prune"])
        .stdout().contains("Pushing updated RSL to remote")
        .unwrap();

    // The test-pr branch should still exist
    Assert::command(&["git", "branch"])
        .with_env(&fixture.env)
        .stdout().contains("test-pr")
        .unwrap();

    // ... and should be the current branch
    Assert::command(&["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .with_env(&fixture.env)
        .stdout().contains("test-pr")
        .unwrap();
}
