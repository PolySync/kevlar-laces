use git_rsl::{prep_workspace, restore_workspace};
use git2;
use std::path::PathBuf;
use errors::*;

pub struct Workspace {
    repo: git2::Repository,
    original_branch_name: String,
    stash_id: Option<git2::Oid>,
    original_dir: Option<PathBuf>
}

impl Workspace {
    pub fn new(mut repo: git2::Repository) -> Result<Workspace> {
        let (original_branch_name, stash_id, original_dir) = prep_workspace(&mut repo)?;

        Ok(
            Workspace {
                repo,
                original_branch_name,
                stash_id,
                original_dir
            }
        )
    }
}

impl<'a> Drop for Workspace {
    fn drop(&mut self) {
        restore_workspace(&mut self.repo,
                          &self.original_branch_name,
                          self.stash_id,
                          self.original_dir.clone())
            .unwrap();
    }
}



