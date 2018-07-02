extern crate assert_cli;
use assert_cli::{Assert, Environment};

extern crate tempfile;
extern crate git2;
extern crate git_rsl;

mod fixture;
use fixture::TestFixture;

use git_rsl::{BranchName, RemoteName};

fn create_tag(tag: &str, repo_path: &str, e: &Environment) {
    // make a devel branch
    let branch_name = "devel";
    fixture::runv(&e, &[
        &["git", "checkout", "-b", branch_name],
        &["git", "commit", "--allow-empty", "-m", "The newness"],
        &["git", "tag", "-s", "-m", tag, tag]
    ]);

    let mut repo = git2::Repository::open(repo_path).unwrap();
    git_rsl::secure_push_with_cleanup(&mut repo,
                                      &RemoteName::new("origin"),
                                      &BranchName::new(branch_name)).unwrap();
    let tag_ref = format!("refs/tags/{0}:refs/tags/{0}", tag);
    let mut remote = repo.find_remote("origin").unwrap();
    remote.push(&[tag_ref.as_str()], None).unwrap();
}

#[test]
fn test_promote_succeeds() {
    let fixture = TestFixture::new();
    let tag = "1.2.3-devel.1";
    create_tag(tag, fixture.local_path(), &fixture.env);
    fixture::run(&fixture.env, &["git", "checkout", "master"]);

    Assert::cargo_binary("git-promote")
        .with_env(&fixture.env)
        .with_args(&[tag, "master"])
        .stdout()
        .contains("Pushed release tag")
        .unwrap();
}