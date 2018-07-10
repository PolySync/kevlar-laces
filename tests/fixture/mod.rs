use git2;
use git_rsl::{self, BranchName, RemoteName};
use tempfile::{self, TempDir};
use assert_cli::{Assert, Environment};

#[allow(dead_code)]
pub struct TestFixture {
    origin: TempDir,
    local: TempDir,
    gpg_home: TempDir,
    pub env: Environment
}

use std::fs::File;
use std::io::Write;

fn write_gpg_keygen_script(out_path: &str) {
    let mut f = File::create(out_path).unwrap();
    f.write_all("%no-protection\n\
                 %transient-key\n\
                 Key-Type: DSA\n\
                 Key-Length: 1024\n\
                 Name-Email: test_user@polysync.io\n\
                 Expire-Date: 0\n\
                 %commit\n".as_bytes()
    ).unwrap();
}

use std::process::Command;
fn first_gpg_key_id(gpghome: &str) -> String {
    let out = Command::new("gpg2")
        .env("GNUPGHOME", gpghome)
        .args(vec!["--with-colons", "--list-keys"])
        .output()
        .unwrap();

    // This splits out lines of this form:
    //    "pub:u:1024:17:31BC51B4BB930CA9:1528761082:::u:::scaSCA:::::::"
    // Keep the one that starts with 'pub', and take the 5th field.

    String::from_utf8_lossy(&out.stdout)
        .lines().filter(|l| l.starts_with("pub"))
        .next().unwrap()
        .split(":")
        .skip(4)
        .next().unwrap().to_string()
}


pub fn run(e: &Environment, args: &[&str]) {
    Assert::command(args).with_env(e).unwrap()
}

pub fn runv(e: &Environment, lines: &[&[&str]]) {
    for line in lines {
        run(e, line);
    }
}

use std::env;

impl TestFixture {
    pub fn new() -> TestFixture {
        let origin = tempfile::Builder::new().prefix("origin").tempdir().unwrap();
        let local = tempfile::Builder::new().prefix("local").tempdir().unwrap();
        let gpg_home = tempfile::Builder::new().prefix("gpg").tempdir().unwrap();

        let e = Environment::inherit()
            .insert("GIT_WORK_TREE", local.path().to_str().unwrap().clone())
            .insert("GIT_DIR", &format!("{}/.git", local.path().to_str().unwrap().clone()))
            .insert("GNUPGHOME", gpg_home.path().to_str().unwrap().clone());


        // This is needed for our local rsl invocations
        env::set_var("GNUPGHOME", gpg_home.path().to_str().unwrap().clone());

        {
            let origin_path = origin.path().to_str().unwrap();
            let local_path = local.path().to_str().unwrap();
            let gpg_home_path = gpg_home.path().to_str().unwrap();

            Assert::command(&["git", "init", "--bare"])
                .with_env(&[("GIT_DIR", origin_path)])
                .unwrap();

            let foo_path = &format!("{}/foo", local_path);

            write_gpg_keygen_script("gpgscript");

            runv(&e, &[
                &["chmod", "0700", gpg_home_path],
                &["gpg2", "--gen-key", "--batch", "gpgscript"],
            ]);

            // find the key id
            let key_id=first_gpg_key_id(gpg_home_path);

            runv(&e, &[
                &["git", "init", local_path],
                &["git", "config", "user.name", "Test User"],
                &["git", "config", "user.email", "test_user@polysync.io"],
                &["git", "config", "gpg.program", "gpg2"],
                &["git", "config", "user.signingKey", key_id.as_str()],
                &["git", "config", "commit.gpgSign", "true"],

                &["touch", foo_path],
                &["git", "add", foo_path],
                &["git", "commit", "-m", "initial revision"],
                &["git", "remote", "add", "origin", origin_path]
            ]);

            let mut local_repo = git2::Repository::open(local_path).unwrap();

            let origin = RemoteName::new("origin");
            git_rsl::rsl_init_with_cleanup(&mut local_repo, &origin).unwrap();

            git_rsl::secure_push_with_cleanup(&mut local_repo,
                                              &origin,
                                              &BranchName::new("master")).unwrap();
        }

        TestFixture { origin, local, gpg_home, env: e }
    }

    pub fn local_path(&self) -> &str {
        self.local.path().to_str().unwrap()
    }
}
