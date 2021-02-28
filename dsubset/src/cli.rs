use clap::Clap;
use std::path::PathBuf;

#[derive(Clap, Debug)]
#[clap(
    version = "0.8",
    author = "jaan-c",
    about = "Check if SUBDIR's descendant files are a subset of SUPERDIR.",
    after_help = "Files are only compared by SHA256 checksum, hence this program does not guarantee that all duplicate files in SUBDIR exists in SUPERDIR.",
    max_term_width = 80
)]
pub struct Args {
    #[clap(value_name = "SUBDIR")]
    pub sub_dir: PathBuf,

    #[clap(value_name = "SUPERDIR")]
    pub super_dir: PathBuf,
}

pub fn get_args() -> Args {
    Args::parse()
}
