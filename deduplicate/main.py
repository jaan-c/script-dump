from files import list_descendant_files, FileInfo
from duplicates import find_duplicates

if __name__ == "__main__":
    root_dir_path = "/home/beep/Documents/Books"

    print("Building file list.")
    infos = list_descendant_files(root_dir_path)

    print("Finding duplicates.")
    duplicates = find_duplicates(infos)

    import pprint

    pprint.pprint(duplicates)
