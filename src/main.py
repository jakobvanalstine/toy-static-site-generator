from textnode import TextType, TextNode
from pathfuncs import is_in_project_root
from remake_public import remake_public


def main():
    if not is_in_project_root():
        raise RuntimeError("script must be executed while in project root")

    remake_public()


if __name__ == "__main__":
    main()
