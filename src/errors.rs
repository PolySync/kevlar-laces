error_chain!{
    links {
        Rsl(::git_rsl::errors::Error, ::git_rsl::errors::ErrorKind);
    }

    foreign_links {
        Git(::git2::Error);
        IO(::std::io::Error);
        Time(::std::time::SystemTimeError);
    }

    errors {
    }
}

pub fn report_error(e: &Error) {
    println!("error: {}", e);
    for e in e.iter().skip(1) {
        println!("caused by: {}", e);
    }
    if let Some(backtrace) = e.backtrace() {
        println!("backtrace: {:?}", backtrace);
    }
}
