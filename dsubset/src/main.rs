mod cli;
mod filesystem;
mod hash;

use hashbrown::HashSet;
use std::io;

fn main() {
    let args = cli::get_args();

    let sub_dir = args.sub_dir;
    let super_dir = args.super_dir;

    println!("Collecting SUBDIR files...");
    let sub_dir_files = filesystem::walk_files(&sub_dir).filter_map(omit_and_log_errors);
    println!("Collecting SUPERDIR files...");
    let super_dir_files = filesystem::walk_files(&super_dir).filter_map(omit_and_log_errors);

    let sub_dir_file_hashes = sub_dir_files
        .map(|f| match hash::file(&f) {
            Ok(h) => Ok((f, h)),
            Err(err) => Err(err),
        })
        .filter_map(omit_and_log_errors); // Intentionally lazy.
    println!("Hashing SUPERDIR files...");
    let super_dir_hashes = super_dir_files
        .into_iter()
        .map(|f| hash::file(f))
        .filter_map(omit_and_log_errors)
        .collect::<HashSet<String>>();

    println!("Checking files...");
    for (sub_file, sub_hash) in sub_dir_file_hashes {
        if !super_dir_hashes.contains(&sub_hash) {
            println!("{} not in {}", sub_file.display(), super_dir.display());
        }
    }
}

fn omit_and_log_errors<T>(result: io::Result<T>) -> Option<T> {
    match result {
        Ok(value) => Some(value),
        Err(err) => {
            println!("{}", err);
            None
        }
    }
}
