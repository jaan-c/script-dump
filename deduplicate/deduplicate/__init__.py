if __name__ == "__main__":
    import sys
    import cli

    cli.execute(sys.argv)
else:
    from .duplicate import find_duplicates
    from .delete import delete_duplicates
    from . import keep
    from . import fileinfo
