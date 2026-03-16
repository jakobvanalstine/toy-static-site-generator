import os

from config import PROJECT_ROOT

__all__ = ["is_in_project_root"]


def is_in_project_root():
    return PROJECT_ROOT == os.path.abspath(os.getcwd())
