import os
import shutil
import logging

from blockfuncs import markdown_to_html_node

__all__ = ["copy_static_to_public", "generate_pages"]


def copy_static_to_public(public_directory, static_directory, basepath):
    if basepath:
        public_directory = os.path.normpath(public_directory + basepath)
    if not os.path.exists(static_directory):
        raise FileNotFoundError(f'"{static_directory}" does not exist')
    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)
    logging.info(f"remaking {public_directory}")
    os.makedirs(public_directory)

    paths_to_check = [static_directory]
    subdirectories = []
    files_to_copy = []
    branches_to_mirror = []
    while paths_to_check:
        path = paths_to_check.pop()
        with os.scandir(path) as directory:
            subdirectories.clear()
            for entry in directory:
                if entry.is_dir(follow_symlinks=False):
                    subdirectories.append(entry.path)
                if entry.is_file(follow_symlinks=False):
                    files_to_copy.append(entry.path)
            if not subdirectories:
                branches_to_mirror.append(path)
            else:
                paths_to_check.extend(subdirectories)

    for branch in branches_to_mirror:
        branch = os.path.relpath(path, static_directory)
        equivalent_for_public = os.path.join(public_directory, branch)
        if not os.path.exists(equivalent_for_public):
            logging.info(f'mirroring "{branch}" as "{equivalent_for_public}"')
            os.makedirs(equivalent_for_public)

    for file in files_to_copy:
        relative_filename = os.path.relpath(file, static_directory)
        equivalent_for_public = os.path.join(
            public_directory, relative_filename
        )
        logging.info(f'copying "{file}" to "{equivalent_for_public}"')
        shutil.copy(file, equivalent_for_public)


def extract_title(markdown):
    if markdown[0] == "#":
        title_start = markdown.index("# ") + 2
    else:
        title_start = markdown.index("\n# ") + 3
    title_finish = markdown.index("\n\n", title_start)
    title = markdown[title_start:title_finish].strip()
    return title


def _generate_page(from_path, template_path, dest_path, basepath):
    logging.info(
        f'Generating "{from_path}" to "{dest_path}" using "{template_path}"'
    )

    if not os.path.exists(from_path):
        raise FileNotFoundError(f'"{from_path}" does not exist')
    with open(from_path, "r") as file:
        markdown = file.read()

    if not os.path.exists(template_path):
        raise FileNotFoundError(f'"{template_path}" does not exist')
    with open(template_path, "r") as file:
        template = file.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)

    content = template.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html)
    content = content.replace('href="/', f'href="{basepath}')
    content = content.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w+") as file:
        file.write(content)


def generate_pages(from_directory, template_path, dest_directory, basepath):
    if basepath:
        dest_directory = os.path.normpath(dest_directory + basepath)
    if not os.path.exists(from_directory):
        raise FileNotFoundError(f'"{from_directory}" does not exist')
    if not os.path.exists(dest_directory):
        raise FileNotFoundError(f'"{dest_directory}" does not exist')

    paths_to_check = [from_directory]
    subdirectories = []
    files_to_copy = []
    branches_to_mirror = []
    while paths_to_check:
        path = paths_to_check.pop()
        with os.scandir(path) as directory:
            subdirectories.clear()
            for entry in directory:
                if entry.is_dir(follow_symlinks=False):
                    subdirectories.append(entry.path)
                if entry.is_file(follow_symlinks=False):
                    files_to_copy.append(entry.path)
            if not subdirectories:
                branches_to_mirror.append(path)
            else:
                paths_to_check.extend(subdirectories)

    for branch in branches_to_mirror:
        branch = os.path.relpath(branch, from_directory)
        equivalent_for_dest = os.path.join(dest_directory, branch)
        if not os.path.exists(equivalent_for_dest):
            logging.info(f'mirroring "{branch}" as "{equivalent_for_dest}"')
            os.makedirs(equivalent_for_dest)

    for file in files_to_copy:
        relative_filename = os.path.relpath(file, from_directory)
        equivalent_for_dest = os.path.join(
            dest_directory, relative_filename.replace(".md", ".html")
        )
        logging.info(f'copying "{file}" to "{equivalent_for_dest}"')
        _generate_page(file, template_path, equivalent_for_dest, basepath)
