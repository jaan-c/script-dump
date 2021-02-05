use core::panic;
use std::path::PathBuf;

#[derive(Debug)]
pub struct Duplicate {
    pub hash: String,
    pub files: Vec<PathBuf>,
}

impl Duplicate {
    pub fn new(hash: String, files: Vec<PathBuf>) -> Duplicate {
        if files.len() < 2 {
            panic!("files length must be greater than 2.");
        }

        Duplicate {
            hash: hash,
            files: files,
        }
    }
}
