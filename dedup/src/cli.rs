use crate::keep::KeepCriteria;
use pico_args as pico;
use std::path::{Path, PathBuf};
use std::process;
use std::str::FromStr;

const HELP: &str = "\
dedup 0.8
jaan-c
Find and delete duplicate files.

USAGE:
    dedup [OPTIONS] PATH...

OPTIONS:
    -h, --help          Displays help information.
    -v, --version       Displays version information.
    -d, --dry-run       Output only and don't perform any deletion.
    -k, --keep-criteria [oldest, newest, shallowest, deepest]
                        Criteria of which file to keep from duplicates. Defaults
                        to newest.
";
const VERSION: &str = "dedup 0.8";

#[derive(Debug)]
pub struct Args {
    pub paths: Vec<PathBuf>,
    pub dry_run: bool,
    pub keep_criteria: KeepCriteria,
}

pub fn get_args() -> Args {
    match parse_args() {
        Ok(args) => args,
        Err(err) => {
            println!("{}", err);
            print!("{}", HELP);
            process::exit(0);
        }
    }
}

fn parse_args() -> Result<Args, pico::Error> {
    let mut pargs = pico::Arguments::from_env();

    if pargs.contains(["-h", "--help"]) {
        print!("{}", HELP);
        process::exit(0);
    } else if pargs.contains(["-h", "--version"]) {
        println!("{}", VERSION);
        process::exit(0);
    }

    let dry_run = pargs.contains(["-d", "--dry-run"]);
    let keep_criteria = pargs
        .opt_value_from_str(["-k", "--keep-criteria"])?
        .unwrap_or(KeepCriteria::Newest);
    let paths = pargs
        .finish()
        .into_iter()
        .map(|s| Path::new(&s).to_path_buf())
        .collect();

    Ok(Args {
        paths,
        dry_run,
        keep_criteria,
    })
}

impl FromStr for KeepCriteria {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "oldest" => Ok(KeepCriteria::Oldest),
            "newest" => Ok(KeepCriteria::Newest),
            "shallowest" => Ok(KeepCriteria::Shallowest),
            "deepest" => Ok(KeepCriteria::Deepest),
            _ => Err(format!("invalid keep criteria '{}'.", s)),
        }
    }
}
