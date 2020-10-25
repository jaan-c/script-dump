use crate::fileinfo;
use hashbrown::HashMap;
use std::fs;
use std::hash::Hash;
use std::io;
use std::ops::Fn;
use std::path::{Path, PathBuf};

pub fn duplicates(dir_path: &Path) -> HashMap<String, Vec<PathBuf>> {
    let file_paths = descendant_files(dir_path);

    let file_paths =
        group_ungroup(file_paths, |fp| fileinfo::size(fp).unwrap_or(0), 0);

    let file_paths = group_ungroup(
        file_paths,
        |fp| fileinfo::head_hash(fp).unwrap_or(String::from("")),
        String::from(""),
    );

    let mut hash_groups = group_by(file_paths, |fp| {
        fileinfo::hash(fp).unwrap_or(String::from(""))
    });
    remove_key_and_singletons(&mut hash_groups, String::from(""));

    hash_groups
}

fn descendant_files(dir_path: &Path) -> Vec<PathBuf> {
    let mut file_paths = Vec::new();
    let handle_error = |e| eprintln!("{}", e);
    collect_files(&mut file_paths, dir_path, &handle_error)
        .unwrap_or_else(&handle_error);
    file_paths
}

fn collect_files<F>(
    buffer: &mut Vec<PathBuf>,
    path: &Path,
    handle_error: &F,
) -> io::Result<()>
where
    F: Fn(io::Error),
{
    if path.is_file() {
        buffer.push(PathBuf::from(path));
        return Ok(());
    }

    for entry in fs::read_dir(path)? {
        let p = entry?.path();
        collect_files(buffer, &p, handle_error).unwrap_or_else(handle_error);
    }

    Ok(())
}

fn group_ungroup<F, K>(
    file_paths: Vec<PathBuf>,
    derive_key: F,
    invalid_key: K,
) -> Vec<PathBuf>
where
    F: Fn(&PathBuf) -> K,
    K: Eq + Hash,
{
    let mut groups = group_by(file_paths, derive_key);
    remove_key_and_singletons(&mut groups, invalid_key);
    groups.drain().map(|(_, ps)| ps).flatten().collect()
}

fn group_by<I, F, K>(paths: I, derive_key: F) -> HashMap<K, Vec<PathBuf>>
where
    I: IntoIterator<Item = PathBuf>,
    F: Fn(&PathBuf) -> K,
    K: Eq + Hash,
{
    let mut path_groups = HashMap::new();
    for p in paths {
        let key = derive_key(&p);
        let group = path_groups.entry(key).or_insert(vec![]);
        group.push(p);
    }

    path_groups
}

fn remove_key_and_singletons<K>(
    file_groups: &mut HashMap<K, Vec<PathBuf>>,
    invalid_key: K,
) where
    K: Eq + Hash,
{
    file_groups.remove(&invalid_key);
    file_groups.retain(|_, ps| ps.len() != 1);
}
