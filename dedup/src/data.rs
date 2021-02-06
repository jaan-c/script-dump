use std::path::PathBuf;

#[derive(Debug)]
pub struct Duplicate {
    pub hash: String,
    pub files: Vec<PathBuf>,
}

impl Duplicate {
    pub fn new(hash: String, files: Vec<PathBuf>) -> Duplicate {
        if files.len() < 2 {
            panic!("files length must be greater than 2.");
        }

        Duplicate {
            hash: hash,
            files: files,
        }
    }
}

#[cfg(test)]
mod tests {
    use std::path::Path;

    use super::Duplicate;

    #[test]
    fn duplicate_new() {
        let dup = Duplicate::new(
            "Hello".to_string(),
            vec![
                Path::new("Hello").to_path_buf(),
                Path::new("World").to_path_buf(),
            ],
        );

        assert_eq!(dup.hash, "Hello");
        assert_eq!(
            dup.files,
            vec![
                Path::new("Hello").to_path_buf(),
                Path::new("World").to_path_buf(),
            ]
        );
    }

    #[test]
    #[should_panic]
    fn duplicate_new_invalid_files() {
        Duplicate::new("Hello".to_string(), vec![Path::new("Hello").to_path_buf()]);
    }
}
