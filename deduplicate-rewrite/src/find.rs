use crate::fileinfo;
use hashbrown::HashMap;
use std::fs;
use std::hash::Hash;
use std::io;
use std::ops::Fn;
use std::path::{Path, PathBuf};

pub fn duplicates<P>(dir_path: P) -> HashMap<String, Vec<PathBuf>>
where
    P: AsRef<Path>,
{
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

fn descendant_files<P>(dir_path: P) -> Vec<PathBuf>
where
    P: AsRef<Path>,
{
    let mut file_paths = Vec::new();
    let handle_error = |e| eprintln!("{}", e);
    collect_files(&mut file_paths, dir_path, &handle_error)
        .unwrap_or_else(&handle_error);
    file_paths
}

fn collect_files<F, P>(
    buffer: &mut Vec<PathBuf>,
    path: P,
    handle_error: &F,
) -> io::Result<()>
where
    F: Fn(io::Error),
    P: AsRef<Path>,
{
    if path.as_ref().is_file() {
        buffer.push(path.as_ref().to_path_buf());
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
    groups.into_iter().map(|(_, ps)| ps).flatten().collect()
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

#[cfg(test)]
mod tests {
    use crate::fileinfo;
    use crate::test_util as util;
    use hashbrown::HashMap;
    use std::path::PathBuf;

    #[test]
    fn duplicate_test() {
        let head1 = util::random_bytes(1024);
        let head2 = util::random_bytes(1024);
        let body1 = util::random_bytes(1024);
        let body2 = util::random_bytes(1024);

        let dir = util::temp_dir();
        let dup1 =
            util::temp_file_with_content_in(&dir, &combine(&head1, &body1));
        let dup2 =
            util::temp_file_with_content_in(&dir, &combine(&head1, &body1));
        let _dup_head1 =
            util::temp_file_with_content_in(&dir, &combine(&head2, &body1));
        let _dup_head2 =
            util::temp_file_with_content_in(&dir, &combine(&head2, &body2));
        let _zero1 = util::temp_random_file_in(&dir, 0);
        let _zero2 = util::temp_random_file_in(&dir, 0);
        let _random1 = util::temp_random_file_in(&dir, 2048);
        let _random2 = util::temp_random_file_in(&dir, 2048);

        let duplicates = super::duplicates(&dir);
        assert!(
            are_groups_eq(
                &duplicates,
                &vec![(
                    fileinfo::hash(&dup1).unwrap(),
                    vec![dup1.path().to_path_buf(), dup2.path().to_path_buf()]
                )]
                .into_iter()
                .collect::<HashMap<String, Vec<PathBuf>>>()
            ),
            "duplicates only returns full equal files, ignores partial equal \
            and zero-byte files"
        );
    }

    fn combine(xs: &[u8], ys: &[u8]) -> Vec<u8> {
        vec![xs.to_vec(), ys.to_vec()]
            .into_iter()
            .flatten()
            .collect()
    }

    fn are_groups_eq(
        gs: &HashMap<String, Vec<PathBuf>>,
        hs: &HashMap<String, Vec<PathBuf>>,
    ) -> bool {
        gs.len() == hs.len()
            && are_items_eq(&gs.keys().collect(), &hs.keys().collect())
            && gs.keys().all(|k| are_items_eq(&gs[k], &hs[k]))
    }

    fn are_items_eq<T>(xs: &Vec<T>, ys: &Vec<T>) -> bool
    where
        T: Eq,
    {
        xs.len() == ys.len() && xs.iter().all(|x| ys.contains(x))
    }
}
