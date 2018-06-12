extern crate assert_cli;
use assert_cli::{Assert, Environment};

extern crate tempfile;
extern crate git2;
extern crate git_rsl;

mod fixture;
use fixture::TestFixture;

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
    git_rsl::secure_push_with_cleanup(&mut gr, pr_name, "origin").unwrap();
}


#[test]
fn test_basic() {
    let fixture = TestFixture::new();

    create_pr(&fixture.env, fixture.local_path(), "test-pr");
    fixture::run(&fixture.env, &["git", "checkout", "master"]);

    // merge it

    Assert::cargo_binary("git-merge-pr")
        .with_env(&fixture.env)
        .with_args(&["test-pr", "master"])
        .stdout().contains("Pushing updated RSL to remote")
        .unwrap();
}
