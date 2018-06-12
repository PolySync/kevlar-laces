extern crate git2;
extern crate git_rsl;

#[macro_use]
extern crate error_chain;

#[macro_use]
extern crate structopt;

mod errors;

use git_rsl::Workspace;
use git_rsl::fetch::secure_fetch;
use git_rsl::push::secure_push;
use git_rsl::utils::git;

use errors::*;
use structopt::StructOpt;

#[derive(StructOpt, Debug)]
#[structopt(name = "git merge-pr")]
struct Opt {
    /// Keep a local copy of the branch to be merged
    #[structopt(long="no-prune")]
    no_prune: bool,

    /// The branch to merge
    #[structopt(name="src")]
    branch_to_merge: String,

    /// The destination branch
    #[structopt(name="dest")]
    destination_branch: String,

}

fn merge_pr(opts: Opt) -> Result<()> {
    let mut repo = git::discover_repo()?;

    let current_branch_name = repo.head()?
        .name()
        .ok_or("Not on a named branch. Please switch to one so we can put \
                you back where you started when this is all through.")?
        .to_owned();

    if !opts.no_prune && current_branch_name == opts.branch_to_merge {
        bail!("You are checked out on the branch you are trying to merge. \
               This will prevent the tool from auto-pruning after merging. \
               If you want to keep a local copy of this branch, please consider \
               the --no-prune flag. Otherwise, check out a different branch \
               and try again.");
    }

    let ws = Workspace::new(&mut repo)?;

    // secure-fetch src, dest
    let mut remote = ws.repo.find_remote("origin")
        .chain_err(|| "unable to find remote 'origin'")?;

    // secure fetch both branches from origin
    secure_fetch(&ws.repo,
                 &mut remote,
                 &vec![opts.branch_to_merge.as_str(),
                       opts.destination_branch.as_str()])?;

    let local_destination_branch = &format!("refs/heads/{}", opts.destination_branch);

    let origin_destination_branch = &format!("refs/remotes/origin/{}", opts.destination_branch);
    let origin_branch_to_merge = &format!("refs/remotes/origin/{}", opts.branch_to_merge);

    let destination_branch_oid = ws.repo.refname_to_id(&origin_destination_branch)?;
    let branch_to_merge_oid = ws.repo.refname_to_id(&origin_branch_to_merge)?;

    let destination_branch_commit = &ws.repo.find_commit(destination_branch_oid)?;
    let branch_to_merge_commit = &ws.repo.find_commit(branch_to_merge_oid)?;

    let destination_branch_annotated_commit = &ws.repo.find_annotated_commit(destination_branch_oid)?;
    let branch_to_merge_annotated_commit = &ws.repo.find_annotated_commit(branch_to_merge_oid)?;

    // The original shell version runs 'git gc' here; I'm omitting it because it
    // gc is a potentially destructive operation, and doing it automatically is
    // somewhat dangerous.

    // Check out the local destination_branch and ff to match the remote, if
    // possible.
    //
    // The shell version did a series of machinations involving a detached HEAD;
    // that won't work here because git-rsl's implementation of secure-push can
    // only push a branch to a remote version of the same name (i.e. you can't
    // push HEAD:branchname, only branchname:branchname)
    ws.repo.set_head(&local_destination_branch)?;

    // secure-fetch leaves the working copy in a crazy state, with the RSL
    // branch checked out, so we need to force checkout the destination branch
    ws.repo.checkout_head(Some(git2::build::CheckoutBuilder::new().force()))?;

    match ws.repo.merge_analysis(&[&destination_branch_annotated_commit])? {
        (git2::MergeAnalysis::ANALYSIS_UP_TO_DATE, _) =>
            println!("local {} branch is up to date", opts.destination_branch),
        (git2::MergeAnalysis::ANALYSIS_FASTFORWARD, _) => {
            println!("fast-forwarding {} to {}", opts.destination_branch,
                     destination_branch_oid);
            git::fast_forward_onto_head(&ws.repo, &origin_destination_branch)?
        },
        _ =>
            bail!("your local {} branch is not in the history of origin/{},\
                   so we can't do a fast-forward merge. You've probably made \
                   a local commit to it. Reconcile the situation (probably by \
                   resetting to origin/{}) and try again.",
                  opts.destination_branch,
                  opts.destination_branch,
                  opts.destination_branch)
    }

    // Stage the merge in the local working copy
    ws.repo.merge(&[&branch_to_merge_annotated_commit],
                  None,
                  None)?;

    // commit the merge
    let signature = ws.repo.signature()?;
    let message = format!("Merge 'origin/{}' into {}",
                          opts.branch_to_merge,
                          opts.destination_branch);
    let tree = ws.repo.head()?.peel_to_tree()?;
    git::commit_signed(
        &ws.repo,
        Some(&local_destination_branch),
        &signature, // author
        &signature, // committer
        &message,
        &tree,
        &[&destination_branch_commit, &branch_to_merge_commit],
    )?;

    // push destination_branch
    secure_push(&ws.repo, &mut remote, &[&opts.destination_branch])?;

    if !opts.no_prune {
        // delete the remote branch by pushing to the ":branch_to_merge"
        // refspec. See git-push(1) for refspec push docs
        git::push_refspecs(&ws.repo, &mut remote,
                           &[&format!(":refs/heads/{}", opts.branch_to_merge)])?;

        // delete the local branch if it exists
        if let Ok(mut branch) = ws.repo.find_branch(&opts.branch_to_merge, git2::BranchType::Local) {
            branch.delete()?
        }
    }

    Ok(())
}

fn main() {
    merge_pr(Opt::from_args()).unwrap();
}
