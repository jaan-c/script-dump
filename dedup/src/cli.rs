use crate::keep::KeepCriteria;
use clap::Clap;
use std::path::PathBuf;
use std::str::FromStr;

#[derive(Clap, Debug)]
#[clap(
    version = "0.8",
    author = "jaan-c",
    about = "Find and delete duplicate files."
)]
pub struct Args {
    #[clap(
        value_name = "PATHS",
        about = "Files or directory to check for duplicate files."
    )]
    pub paths: Vec<PathBuf>,
    #[clap(short, long, about = "Output only and do not perform any deletions.")]
    pub dry_run: bool,
    #[clap(
        short,
        long,
        default_value = "newest",
        possible_values=&["oldest", "newest", "shallowest", "deepest"],
        about = "Criteria of which file to keep from duplicates."
    )]
    pub keep_criteria: KeepCriteria,
}

impl FromStr for KeepCriteria {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "oldest" => Ok(KeepCriteria::Oldest),
            "newest" => Ok(KeepCriteria::Newest),
            "shallowest" => Ok(KeepCriteria::Shallowest),
            "deepest" => Ok(KeepCriteria::Deepest),
            _ => Err(format!("Invalid keep criteria '{}'.", s)),
        }
    }
}

pub fn get_args() -> Args {
    Args::parse()
}
