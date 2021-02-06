use crate::data::Duplicate;
use std::fs;
use std::io;
use std::path::{Component, Path, PathBuf};
use std::time::SystemTime;

#[derive(Debug)]
pub enum KeepCriteria {
    Oldest,
    Newest,
    Shallowest,
    Deepest,
}

pub fn by_criteria(duplicate: &Duplicate, criteria: &KeepCriteria) -> io::Result<PathBuf> {
    match criteria {
        KeepCriteria::Oldest => keep_oldest(&duplicate.files),
        KeepCriteria::Newest => keep_newest(&duplicate.files),
        KeepCriteria::Shallowest => keep_shallowest(&duplicate.files),
        KeepCriteria::Deepest => keep_deepest(&duplicate.files),
    }
}

fn keep_oldest(files: &Vec<PathBuf>) -> io::Result<PathBuf> {
    Ok(sort_by_mod_time(files)?.first().unwrap().clone())
}

fn keep_newest(files: &Vec<PathBuf>) -> io::Result<PathBuf> {
    Ok(sort_by_mod_time(files)?.last().unwrap().clone())
}

fn sort_by_mod_time(files: &Vec<PathBuf>) -> io::Result<Vec<PathBuf>> {
    let mod_times = files
        .iter()
        .map(|f| get_modification_time(f))
        .collect::<io::Result<Vec<SystemTime>>>();
    let mut mod_times_files = mod_times?
        .into_iter()
        .zip(files)
        .collect::<Vec<(SystemTime, &PathBuf)>>();

    mod_times_files.sort_by(|a, b| a.0.cmp(&b.0));

    Ok(mod_times_files
        .into_iter()
        .map(|(_, f)| f.clone())
        .collect())
}

fn get_modification_time<P>(path: P) -> io::Result<SystemTime>
where
    P: AsRef<Path>,
{
    fs::metadata(path)?.modified()
}

fn keep_shallowest(files: &Vec<PathBuf>) -> io::Result<PathBuf> {
    Ok(sort_by_path_depth(files)?.first().unwrap().clone())
}

fn keep_deepest(files: &Vec<PathBuf>) -> io::Result<PathBuf> {
    Ok(sort_by_path_depth(files)?.last().unwrap().clone())
}

fn sort_by_path_depth(files: &Vec<PathBuf>) -> io::Result<Vec<PathBuf>> {
    let depths = files
        .iter()
        .map(|f| get_path_depth(f))
        .collect::<io::Result<Vec<usize>>>()?;
    let mut depths_files = depths
        .into_iter()
        .zip(files)
        .collect::<Vec<(usize, &PathBuf)>>();

    depths_files.sort_by(|a, b| a.0.cmp(&b.0));

    Ok(depths_files.into_iter().map(|(_, f)| f.clone()).collect())
}

fn get_path_depth<P>(path: P) -> io::Result<usize>
where
    P: AsRef<Path>,
{
    Ok(path
        .as_ref()
        .canonicalize()?
        .components()
        .collect::<Vec<Component>>()
        .len())
}
