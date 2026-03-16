from os import getcwd, walk, path

from generate_website import *
import config


def main():
    working_directory = getcwd()
    if working_directory != config.PROJECT_ROOT:
        raise RuntimeError("must execute script from project root")

    copy_static_to_public(config.PATH_TO_PUBLIC, config.PATH_TO_STATIC)
    generate_pages(config.PATH_TO_MARKDOWN, config.PATH_TO_TEMPLATE, config.PATH_TO_PUBLIC)


if __name__ == "__main__":
    main()
