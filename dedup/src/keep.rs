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

pub fn by_criteria<P>(duplicate_files: &[P], criteria: &KeepCriteria) -> io::Result<PathBuf>
where
    P: AsRef<Path>,
{
    match criteria {
        KeepCriteria::Oldest => keep_oldest(duplicate_files),
        KeepCriteria::Newest => keep_newest(duplicate_files),
        KeepCriteria::Shallowest => keep_shallowest(duplicate_files),
        KeepCriteria::Deepest => keep_deepest(duplicate_files),
    }
}

fn keep_oldest<P>(files: &[P]) -> io::Result<PathBuf>
where
    P: AsRef<Path>,
{
    Ok(sort_by_mod_time(files)?.first().unwrap().clone())
}

fn keep_newest<P>(files: &[P]) -> io::Result<PathBuf>
where
    P: AsRef<Path>,
{
    Ok(sort_by_mod_time(files)?.last().unwrap().clone())
}

fn sort_by_mod_time<P>(files: &[P]) -> io::Result<Vec<PathBuf>>
where
    P: AsRef<Path>,
{
    let files = files
        .iter()
        .map(|f| f.as_ref().to_path_buf())
        .collect::<Vec<PathBuf>>();
    let mod_times = files
        .iter()
        .map(|f| get_modification_time(f))
        .collect::<io::Result<Vec<SystemTime>>>();
    let mut mod_times_files = mod_times?
        .into_iter()
        .zip(files)
        .collect::<Vec<(SystemTime, PathBuf)>>();

    mod_times_files.sort_by(|a, b| a.0.cmp(&b.0));

    Ok(mod_times_files.into_iter().map(|(_, f)| f).collect())
}

fn get_modification_time<P>(path: P) -> io::Result<SystemTime>
where
    P: AsRef<Path>,
{
    fs::metadata(path)?.modified()
}

fn keep_shallowest<P>(files: &[P]) -> io::Result<PathBuf>
where
    P: AsRef<Path>,
{
    Ok(sort_by_path_depth(files)?.first().unwrap().clone())
}

fn keep_deepest<P>(files: &[P]) -> io::Result<PathBuf>
where
    P: AsRef<Path>,
{
    Ok(sort_by_path_depth(files)?.last().unwrap().clone())
}

fn sort_by_path_depth<P>(files: &[P]) -> io::Result<Vec<PathBuf>>
where
    P: AsRef<Path>,
{
    let files = files
        .iter()
        .map(|f| f.as_ref().to_path_buf())
        .collect::<Vec<PathBuf>>();
    let depths = files
        .iter()
        .map(|f| get_path_depth(f))
        .collect::<io::Result<Vec<usize>>>()?;
    let mut depths_files = depths
        .into_iter()
        .zip(files)
        .collect::<Vec<(usize, PathBuf)>>();

    depths_files.sort_by(|a, b| a.0.cmp(&b.0));

    Ok(depths_files.into_iter().map(|(_, f)| f).collect())
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
