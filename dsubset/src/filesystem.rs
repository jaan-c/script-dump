use std::fs;
use std::io;
use std::iter::Iterator;
use std::path::{Path, PathBuf};

// An [Iterator] that yields all descendant files of a directory.
//
// Symlinks are silently ignored.
pub struct FileWalker {
    pending_yield: Vec<io::Result<PathBuf>>,
    parents: Vec<PathBuf>,
}

impl FileWalker {
    pub fn new<P>(directory: P) -> FileWalker
    where
        P: AsRef<Path>,
    {
        FileWalker {
            pending_yield: vec![],
            parents: vec![directory.as_ref().to_path_buf()],
        }
    }
}

impl Iterator for FileWalker {
    type Item = io::Result<PathBuf>;

    fn next(&mut self) -> Option<Self::Item> {
        if !self.pending_yield.is_empty() {
            let first = self.pending_yield.remove(0);
            return Some(first);
        }

        if self.parents.is_empty() {
            return None;
        }

        let mut new_pending_yield = vec![] as Vec<io::Result<PathBuf>>;
        let mut new_parents = vec![];
        for p in self.parents.iter() {
            let (files, dirs, errs) = partition_directory_children(p);

            new_parents.extend(dirs);

            new_pending_yield.extend(files.into_iter().map(|f| Ok(f)));
            new_pending_yield.extend(errs.into_iter().map(|e| Err(e)));
        }

        self.pending_yield = new_pending_yield;
        self.parents = new_parents;

        if !self.pending_yield.is_empty() {
            let first = self.pending_yield.remove(0);
            Some(first)
        } else {
            self.next()
        }
    }
}

/// Partition children of directory into a tuple (files, dirs, errors).
fn partition_directory_children<P>(directory: P) -> (Vec<PathBuf>, Vec<PathBuf>, Vec<io::Error>)
where
    P: AsRef<Path>,
{
    let mut files = vec![];
    let mut dirs = vec![];
    let mut errors = vec![];

    let entries = match fs::read_dir(directory) {
        Ok(entries) => entries,
        Err(err) => return (files, dirs, vec![err]),
    };

    for entry in entries {
        match entry {
            Ok(entry) => match entry.metadata() {
                Ok(metadata) => {
                    if metadata.is_dir() {
                        dirs.push(entry.path());
                    } else if metadata.is_file() {
                        files.push(entry.path());
                    } else {
                        println!("Ignoring symlink {}", entry.path().display());
                    }
                }
                Err(err) => errors.push(err),
            },
            Err(err) => errors.push(err),
        };
    }

    (files, dirs, errors)
}

pub fn walk_files<P>(directory: P) -> FileWalker
where
    P: AsRef<Path>,
{
    FileWalker::new(directory)
}
