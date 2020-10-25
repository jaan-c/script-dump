use std::fs;
use std::hash::Hash;
use std::path::PathBuf;

pub fn duplicates<K, F>(
    duplicate_paths: Vec<PathBuf>,
    keep_filter: F,
) -> Result<(), String>
where
    K: Eq + Hash,
    F: Fn(&Vec<PathBuf>) -> Vec<bool>,
{
    let filter = keep_filter(&duplicate_paths);
    assert_eq!(duplicate_paths.len(), filter.len());

    for (path, should_keep) in duplicate_paths.iter().zip(filter) {
        if !should_keep {
            fs::remove_file(path).unwrap_or_else(|e| {
                eprintln!("Failed to delete {}: {}", path.display(), e)
            });
        }
    }

    Ok(())
}
