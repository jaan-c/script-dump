use pico_args as pico;
use std::path::PathBuf;
use std::process;

const HELP: &str = "\
dsubset 0.8
jaan-c
Check if SUBDIR's descendant files are a subset of SUPERDIR checksum.

USAGE:
    dsubset SUBDIR SUPERDIR

OPTIONS:
    -h, --help          Displays help information.
    -v, --version       Displays version information.";
const VERSION: &str = "dsubset 0.8";

#[derive(Debug)]
pub struct Args {
    pub sub_dir: PathBuf,
    pub super_dir: PathBuf,
}

pub fn get_args() -> Args {
    match parse_args() {
        Ok(args) => args,
        Err(err) => {
            eprintln!("{}", err);
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
    } else if pargs.contains(["-v", "--version"]) {
        println!("{}", VERSION);
        process::exit(0);
    }

    let args = Args {
        sub_dir: pargs.free_from_str()?,
        super_dir: pargs.free_from_str()?,
    };

    let remaining = pargs.finish();
    if !remaining.is_empty() {
        eprintln!("Invalid excess arguments: {:?}", remaining);
        println!("{}", HELP);
        process::exit(0);
    }

    Ok(args)
}
