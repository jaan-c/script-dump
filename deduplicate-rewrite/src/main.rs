mod delete;
mod fileinfo;
mod find;

fn main() {}

#[cfg(test)]
mod test_utils {
    use rand::Rng;
    use std::fs::File;
    use std::io::{Seek, SeekFrom, Write};
    use std::path::Path;
    use tempfile::{NamedTempFile, TempDir};

    pub fn temp_dir() -> TempDir {
        TempDir::new().unwrap()
    }

    pub fn temp_random_file_in<P>(dir: P, size: usize) -> NamedTempFile
    where
        P: AsRef<Path>,
    {
        temp_file_with_content_in(dir, &random_bytes(size))
    }

    pub fn temp_file_with_content_in<P>(dir: P, content: &[u8]) -> NamedTempFile
    where
        P: AsRef<Path>,
    {
        let mut file = NamedTempFile::new_in(dir).unwrap();
        write_and_seek_0(file.as_file_mut(), content);
        file
    }

    pub fn temp_random_file(size: usize) -> NamedTempFile {
        temp_file_with_content(&random_bytes(size))
    }

    pub fn temp_file_with_content(content: &[u8]) -> NamedTempFile {
        let mut file = NamedTempFile::new().unwrap();
        write_and_seek_0(file.as_file_mut(), content);
        file
    }

    pub fn write_and_seek_0(file: &mut File, content: &[u8]) {
        file.write(content).unwrap();
        file.flush().unwrap();
        file.sync_all().unwrap(); // Sync metadata with file content change.
        file.seek(SeekFrom::Start(0)).unwrap();
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
