
error_chain!{
    foreign_links {
        Rsl(::git_rsl::errors::Error);
        Git(::git2::Error);
        // Serde(::serde_json::Error);
        // GPGME(::gpgme::Error);
        IO(::std::io::Error);
        Time(::std::time::SystemTimeError);
    }

    errors {
    }
}
