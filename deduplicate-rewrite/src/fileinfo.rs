use crypto_hash::{self, Algorithm, Hasher};
use hex;
use std::fs::{self, File};
use std::io::Write;
use std::io::{self, BufReader, Read};
use std::path::Path;
use std::time::SystemTime;

const BUFFER_SIZE: usize = 1024;
const HASH_ALGORITHM: Algorithm = Algorithm::SHA256;

pub fn size<P>(file_path: P) -> io::Result<u64>
where
    P: AsRef<Path>,
{
    Ok(fs::metadata(file_path)?.len())
}

pub fn modification_time<P>(file_path: P) -> io::Result<SystemTime>
where
    P: AsRef<Path>,
{
    fs::metadata(file_path)?.modified()
}

pub fn head_hash<P>(file_path: P) -> io::Result<String>
where
    P: AsRef<Path>,
{
    let mut buf = [0; BUFFER_SIZE];
    let count = File::open(file_path)?.read(&mut buf)?;
    Ok(crypto_hash::hex_digest(HASH_ALGORITHM, &buf[..count]))
}

pub fn hash<P>(file_path: P) -> io::Result<String>
where
    P: AsRef<Path>,
{
    let mut buf = [0; BUFFER_SIZE];
    let mut hasher = Hasher::new(HASH_ALGORITHM);

    let file = File::open(file_path)?;
    let mut file = BufReader::with_capacity(4_000_000, file); // 4 MB
    loop {
        match file.read(&mut buf)? {
            0 => break,
            count => hasher.write(&buf[..count])?,
        };
    }

    Ok(hex::encode(hasher.finish()))
}

#[cfg(test)]
mod tests {
    use crate::test_util as util;
    use filetime::{self, FileTime};
    use std::time::SystemTime;

    #[test]
    fn size_test() {
        let file = util::temp_random_file(1024);
        let zero_file = util::temp_random_file(0);

        assert_eq!(super::size(&file).unwrap(), 1024);
        assert_eq!(super::size(&zero_file).unwrap(), 0);
    }

    #[test]
    fn modification_time_test() {
        let old_file = util::temp_random_file(1024);
        let now_file = util::temp_random_file(2048);
        let zero = SystemTime::UNIX_EPOCH;
        let now = SystemTime::now();

        filetime::set_file_mtime(&old_file, FileTime::from_system_time(zero))
            .unwrap();
        filetime::set_file_mtime(&now_file, FileTime::from_system_time(now))
            .unwrap();

        assert_eq!(super::modification_time(&old_file).unwrap(), zero);
        assert_eq!(super::modification_time(&now_file).unwrap(), now);
    }

    #[test]
    fn all_hash_test() {
        // ~2048 bytes dummy text.
        let lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum convallis nibh sit amet est faucibus, quis lacinia metus consequat. Sed ac arcu nibh. Integer bibendum turpis est, at venenatis nibh tempor ut. Maecenas mattis felis massa, ac laoreet risus dignissim eget. Donec faucibus id odio quis eleifend. Proin nunc metus, tincidunt maximus nibh ac, ultrices tempus est. Aliquam sollicitudin dui a dolor bibendum pharetra. Vivamus at felis nec turpis posuere feugiat. Maecenas viverra velit a quam aliquam tempor. Donec eros libero, mattis vitae justo ornare, aliquam blandit dui. Pellentesque sit amet metus a tortor malesuada dignissim. Integer vel laoreet ex. Donec quam metus, lobortis eu nulla et, semper aliquet risus. Integer egestas, ipsum vitae ornare rhoncus, felis massa feugiat eros, sit amet gravida odio ipsum a mauris. Suspendisse potenti. Morbi dolor tellus, bibendum a consectetur nec, sagittis id nisi. Sed tempus, ligula vitae malesuada tristique, urna ante gravida elit, eget scelerisque erat turpis bibendum est. Aliquam erat volutpat. Sed rutrum dolor at finibus placerat. Curabitur imperdiet lectus dolor, quis bibendum dui consequat in. Duis pharetra sem a velit pulvinar, in laoreet purus aliquet. Maecenas dignissim tristique orci a aliquet. Fusce dictum sit amet quam ac interdum. Nulla sagittis, neque a molestie tincidunt, diam purus condimentum augue, ut dapibus ipsum elit eget sapien. Vestibulum at magna turpis. Morbi congue purus sit amet augue interdum laoreet at in nulla. Mauris sed libero dolor. Maecenas tempor nunc eros, non pulvinar augue lobortis nec. Nam posuere, nunc ac tristique semper, nibh massa semper orci, at ornare sapien justo quis justo. Duis luctus ipsum ac mi mattis, aliquam vehicula nulla imperdiet. Fusce ac accumsan tellus. Maecenas consequat pharetra ultrices. Nulla sagittis tellus lorem, nec finibus purus consequat sit amet. Nulla facilisi. Maecenas dictum id libero mollis porttitor. Ut vehicula, lorem ac scelerisque cursus, tellus sem tristique lectus, a cursus magna odio et.";
        let file = util::temp_file_with_content(lorem.as_bytes());
        let head_hash = super::head_hash(&file).unwrap();
        let hash = super::hash(&file).unwrap();

        assert_eq!(head_hash.len(), 64);
        assert_eq!(hash.len(), 64);

        assert_ne!(head_hash, hash);

        assert_eq!(head_hash, String::from("85df27113928871d466a47abdfa764ebbc727cd06132bb32aa40aa78a7956e9f"));
        assert_eq!(hash, String::from("a875858b0128bd3ce6d56a7c2696c517b5d0307788d5dfa006a37dd3e478e80f"));
    }
}
