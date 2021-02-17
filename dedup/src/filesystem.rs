use std::fs;
use std::io;
use std::path::{Path, PathBuf};

/// Walk descendant files of directory.
pub fn walk_files<P>(directory: P) -> io::Result<Vec<PathBuf>>
where
    P: AsRef<Path>,
{
    let mut files = vec![];

    let mut parents = vec![directory.as_ref().to_path_buf()];
    while !parents.is_empty() {
        let mut new_parents = vec![];

        for dir in parents {
            let (mut child_files, mut child_dirs) = partition_directory_children(dir)?;
            files.append(&mut child_files);
            new_parents.append(&mut child_dirs);
        }

        parents = new_parents;
    }

    Ok(files)
}

/// Partition children of directory into a pair of files and directories.
fn partition_directory_children<P>(directory: P) -> io::Result<(Vec<PathBuf>, Vec<PathBuf>)>
where
    P: AsRef<Path>,
{
    let children = fs::read_dir(directory)?
        .map(|e| Ok(e?.path()))
        .collect::<io::Result<Vec<PathBuf>>>()?;

    Ok(children.into_iter().partition(|c| c.is_file()))
}
