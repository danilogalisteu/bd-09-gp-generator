import pathlib
import shutil

PATH_SRC = pathlib.Path("./static")
PATH_DST = pathlib.Path("./public")


def build():
    if PATH_DST.exists():
        shutil.rmtree(PATH_DST)

    shutil.copytree(PATH_SRC, PATH_DST)


def main():
    build()


if __name__ == "__main__":
    main()
