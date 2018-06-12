#[macro_use]
extern crate structopt;
#[macro_use]
extern crate error_chain;
#[macro_use]
extern crate lazy_static;
#[macro_use]
extern crate log;
extern crate env_logger;

extern crate git2;
extern crate git_rsl;
extern crate regex;

pub mod errors;

use regex::Regex;
use structopt::StructOpt;
use git_rsl::Workspace;
use git_rsl::utils::git::{
    discover_repo,
    checkout_branch,
    up_to_date,
    fast_forward_possible,
    fast_forward_onto_head,
    commit_signed,
    fetch,
};
use git_rsl::fetch::secure_fetch;
use git_rsl::push::secure_push;
use errors::*;

#[derive(StructOpt, Debug)]
#[structopt(name = "git-promote", author = "Devin Smith <dsmith@polysync.io>")]
struct Opt {
    #[structopt(short = "r", long = "remote", default_value = "origin")]
    remote: String,
    /// The pre-release tag to be promoted
    tag: String,
    /// The target branch to promote to
    branch: String,
}

fn main() {
    env_logger::init();
    info!("Initialized Logger");
    let opt = Opt::from_args();

    if let Err(ref e) = run(&opt) {
        println!("error: {}", e);

        for e in e.iter().skip(1) {
            println!("caused by: {}", e);
        }

        if let Some(backtrace) = e.backtrace() {
            println!("backtrace: {:?}", backtrace);
        }

        ::std::process::exit(1);
    }
}

fn run(options: &Opt) -> Result<()> {
    let mut repo = discover_repo()?;
    let ws = Workspace::new(&mut repo)?;
    let release_tag = parse_release_tag(&options.tag)?;
    debug!("branch: {}, tag: {}, release_tag: {}, remote: {}", options.branch, options.tag, release_tag, options.remote);

    // fetch remote branches and tags for prerelease and target
    let mut remote = (&ws.repo)
        .find_remote(&options.remote)
        .chain_err(|| format!("unable to find remote named {}", &options.remote))?;
    info!("Insecurely fetching tag {}", &options.tag);
    fetch(&ws.repo, &mut remote, &[options.tag.as_str()], None)?; // todo -- move to secure-fetch once support exists for fetching tags
    info!("Fetched {} {}", &options.remote, &options.tag);
    info!("Secure-Fetching origin/{}", &options.branch);
    secure_fetch(&ws.repo, &mut remote, &[options.branch.as_str()])?;
    info!("Fetched {} {}", &options.remote, &options.branch);

    // check out target branch
    info!("Checking out {}", &options.branch);
    checkout_branch(&ws.repo, &format!("refs/heads/{}", &options.branch))?;
    info!("Checked out {}", &options.branch);

    // fast forward latest changes to target branch
    info!("Attempting to fast forward {} to remote head", &options.branch);
    if ! up_to_date(&ws.repo, &options.branch, &format!("origin/{}", &options.branch))? {
        let remote_head = format!("refs/remotes/{}/{}", &options.remote, &options.branch);
        match fast_forward_possible(&ws.repo, &remote_head) {
            Ok(true) => {
                info!("Fast forwarding to {}", remote_head);
                fast_forward_onto_head(&ws.repo, &remote_head)?;
                info!("Local fast forwarded");
            },
            Ok(false) => bail!("Local target branch cannot be fast-forwarded to match remote."),
            Err(e) => Err(e).chain_err(|| "Local target branch cannot be fast-forwarded to match remote.")?,
        }
    } else {
        info!("Local is already up to date");
    }

    let tag_oid = ws.repo.refname_to_id(&format!("refs/tags/{}", &options.tag))?;
    let branch_oid = ws.repo.refname_to_id(&format!("refs/heads/{}", &options.branch))?;
    let tag_commit = ws.repo.find_tag(tag_oid)?.peel()?.peel_to_commit()?;
    let branch_commit = ws.repo.find_commit(branch_oid)?;
    info!("Creating merge of tag: {} onto branch: {}", options.tag, options.branch);
    ws.repo.merge_commits(&branch_commit, &tag_commit, None)?;
    info!("Created merge");

    let signature = ws.repo.signature()?;
    let message = format!("Merge {} into {}", options.tag, options.branch);
    let tree = ws.repo.head()?.peel_to_tree()?;
    info!("Commiting signed merge");
    let update_ref = format!("refs/heads/{}", &options.branch);
    commit_signed(
        &ws.repo,
        Some(update_ref.as_str()),
        &signature,
        &signature,
        &message,
        &tree,
        &[&branch_commit, &tag_commit],
    )?;
    info!("Signed merge commited");

    // tag target HEAD with signed release tag
    let signature = ws.repo.signature()?;
    info!("Creating release tag {}", release_tag);
    let branch_oid = ws.repo.refname_to_id(&format!("refs/heads/{}", &options.branch))?;
    ws.repo.tag(
        &release_tag,
        &ws.repo.find_object(branch_oid, None)?,
        &signature,
        &release_tag,
        false)?;
    info!("Release tag {} created.", release_tag);

    // secure-push origin target_branch
    info!("Securely pushing {} to {}", options.branch, options.remote);
    secure_push(&ws.repo, &mut remote, &[options.branch.as_str()])?;
    info!("Pushed {}", options.branch);
    info!("Insecurely pushing release tag {} to {}", release_tag, options.remote);
    let tag_ref = format!("refs/tags/{0}:refs/tags/{0}", release_tag);
    // Todo -- secure push release tag -- not currently implemented in git-rsl
    remote.push(&[tag_ref.as_str()], None)?;
    info!("Releas tag {} pushed", release_tag);

    Ok(())
}

fn parse_release_tag(tag: &str) -> Result<&str> {
    lazy_static! {
        static ref TAG_PATTERN: Regex = Regex::new("\\d+\\.\\d+\\.\\d+").unwrap();
    }

    if let Some(tag_match) = TAG_PATTERN.find(tag) {
        Ok(tag_match.as_str())
    } else {
        bail!("Unable to parse a release tag from {}", tag)
    }
}
