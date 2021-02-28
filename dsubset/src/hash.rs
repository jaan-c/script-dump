use crypto_hash::{self, Algorithm, Hasher};
use hex;
use std::fs::File;
use std::io;
use std::io::{BufReader, Read, Write};
use std::path::Path;

const BUFFER_SIZE: usize = 4096;
const HASH_ALGORITHM: Algorithm = Algorithm::SHA256;

pub fn file<P>(path: P) -> io::Result<String>
where
    P: AsRef<Path>,
{
    let mut buf = [0; BUFFER_SIZE];
    let mut hasher = Hasher::new(HASH_ALGORITHM);

    let mut reader = BufReader::with_capacity(BUFFER_SIZE * 8, File::open(&path)?);
    loop {
        match reader.read(&mut buf)? {
            0 => break,
            count => hasher.write(&buf[..count])?,
        };
    }

    Ok(hex::encode(hasher.finish()))
}
