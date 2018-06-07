extern crate git2;
extern crate git_rsl;

#[macro_use]
extern crate error_chain;

mod workspace;
mod errors;


use workspace::Workspace;
use git_rsl::{prep_workspace, restore_workspace};
use git_rsl::utils::git::discover_repo;
use errors::*;

fn main() {
    let repo = discover_repo().unwrap(); 
    let ws = Workspace::new(repo).unwrap();

    println!("merge-pr");
}
