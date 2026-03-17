import sys
from os import getcwd, walk, path

from generate_website import *
import config


def main():
    project_root = config.PROJECT_ROOT
    publishing_directory = config.PATH_TO_PUBLIC
    resources_directory = config.PATH_TO_STATIC
    html_template = config.PATH_TO_TEMPLATE
    markdown_directory = config.PATH_TO_MARKDOWN

    basepath = path.join("/", sys.argv[1])

    copy_static_to_public(publishing_directory, resources_directory)
    generate_pages(
        markdown_directory,
        html_template,
        publishing_directory,
        basepath,
    )


if __name__ == "__main__":
    main()
