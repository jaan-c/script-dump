use crate::data::Duplicate;
use crypto_hash::{self, Algorithm, Hasher};
use std::collections::HashMap;
use std::fs;
use std::fs::File;
use std::hash::Hash;
use std::io::{self, BufReader, Read, Write};
use std::path::Path;
use std::path::PathBuf;

const HEAD_SIZE: usize = 4_000;
const FILE_BUFFER_SIZE: usize = 16_000;
const HASH_ALGORITHM: Algorithm = Algorithm::SHA256;

/// Find all duplicate files under directory.
pub fn duplicate_files<P>(directory: P) -> io::Result<Vec<Duplicate>>
where
    P: AsRef<Path>,
{
    let files = descendant_files(directory)?;

    let files = omit_size_singletons(files)?;
    let files = omit_head_hash_singletons(files)?;
    let hash_groups = group_by_hash(files)?;

    Ok(hash_groups
        .into_iter()
        .map(|(h, f)| Duplicate::new(h, f))
        .collect())
}

fn descendant_files<P>(directory: P) -> io::Result<Vec<PathBuf>>
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

fn omit_size_singletons<I>(files: I) -> io::Result<Vec<PathBuf>>
where
    I: IntoIterator<Item = PathBuf>,
{
    let mut size_groups = group_by(files, |f| get_file_size(f))?;
    size_groups.remove(&0);
    Ok(ungroup(omit_singletons(size_groups)))
}

fn omit_head_hash_singletons<I>(files: I) -> io::Result<Vec<PathBuf>>
where
    I: IntoIterator<Item = PathBuf>,
{
    let head_hash_groups = group_by(files, |f| get_head_hash(f))?;
    Ok(ungroup(omit_singletons(head_hash_groups)))
}

fn group_by_hash<I>(files: I) -> io::Result<HashMap<String, Vec<PathBuf>>>
where
    I: IntoIterator<Item = PathBuf>,
{
    let hash_groups = group_by(files, |f| get_hash(f))?;
    Ok(omit_singletons(hash_groups))
}

fn group_by<I, F, K>(files: I, derive_key: F) -> io::Result<HashMap<K, Vec<PathBuf>>>
where
    I: IntoIterator<Item = PathBuf>,
    F: Fn(&PathBuf) -> io::Result<K>,
    K: Eq + Hash,
{
    let mut key_groups = HashMap::new();
    for p in files {
        let key = derive_key(&p)?;
        let group = key_groups.entry(key).or_insert(vec![]);
        group.push(p);
    }

    Ok(key_groups)
}

fn omit_singletons<K>(map: HashMap<K, Vec<PathBuf>>) -> HashMap<K, Vec<PathBuf>>
where
    K: Eq + Hash,
{
    map.into_iter().filter(|(_, g)| g.len() != 1).collect()
}

fn ungroup<K>(map: HashMap<K, Vec<PathBuf>>) -> Vec<PathBuf>
where
    K: Eq,
{
    map.into_iter().map(|(_, g)| g).flatten().collect()
}

fn get_file_size<P>(path: P) -> io::Result<u64>
where
    P: AsRef<Path>,
{
    Ok(fs::metadata(path)?.len())
}

fn get_head_hash<P>(path: P) -> io::Result<String>
where
    P: AsRef<Path>,
{
    let mut buf = [0; HEAD_SIZE];
    let count = File::open(path)?.read(&mut buf)?;
    Ok(crypto_hash::hex_digest(HASH_ALGORITHM, &buf[..count]))
}

fn get_hash<P>(path: P) -> io::Result<String>
where
    P: AsRef<Path>,
{
    let mut buf = [0; HEAD_SIZE];
    let mut hasher = Hasher::new(HASH_ALGORITHM);

    let mut reader = BufReader::with_capacity(FILE_BUFFER_SIZE, File::open(path)?);
    loop {
        match reader.read(&mut buf)? {
            0 => break,
            count => hasher.write(&buf[..count])?,
        };
    }

    Ok(hex::encode(hasher.finish()))
}
