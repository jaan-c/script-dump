mod delete;
mod fileinfo;
mod find;

fn main() {}

#[cfg(test)]
mod test_utils {
    use rand::Rng;
    use std::io::{Seek, SeekFrom, Write};
    use tempfile::NamedTempFile;

    pub fn random_file(size: usize) -> NamedTempFile {
        file_with(&random_bytes(size))
    }

    pub fn file_with(content: &[u8]) -> NamedTempFile {
        let mut file = NamedTempFile::new().unwrap();
        file.write(content).unwrap();
        file.flush().unwrap();
        file.as_file().sync_all().unwrap(); // Sync metadata with file changes.
        file.seek(SeekFrom::Start(0)).unwrap();

        file
    }

    pub fn random_bytes(size: usize) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(size);
        let mut rng = rand::thread_rng();
        for _ in 0..size {
            let b = rng.gen::<u8>();
            bytes.push(b);
        }

        bytes
    }
}
