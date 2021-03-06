mod cli;
mod filesystem;
mod find;
mod keep;

use std::fs;
use std::io;

fn main() -> io::Result<()> {
    let args = cli::get_args();

    let mut files = vec![];
    for p in args.paths {
        if p.is_dir() {
            files.extend(filesystem::walk_files(p)?)
        } else {
            files.push(p)
        }
    }

    let duplicates = find::duplicate_files(files)?;
    for d in duplicates {
        println!("{}", &d.hash);

        let kept = keep::by_criteria(&d.files, &args.keep_criteria)?;
        let for_deletion = d.files.into_iter().filter(|f| *f != kept);

        println!("\tKept {}", kept.display());
        for f in for_deletion {
            if !args.dry_run {
                match fs::remove_file(&f) {
                    Ok(()) => println!("\tDeleted {}", f.display()),
                    Err(error) => println!("\tFailed to delete {}: {}", &f.display(), error),
                }
            } else {
                println!("\tDeleted {}", f.display());
            }
        }
    }

    Ok(())
}
