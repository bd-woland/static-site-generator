import os
import shutil


def copy_dir(src: str, target: str):
    map_dir(src, target, shutil.copy)


def map_dir(src: str, target: str, callback: callable):
    if not os.path.exists(src):
        raise Exception(f'Path "{src}" does not exist.')

    if not os.path.isdir(src):
        raise Exception(f'Path "{src}" is not a directory.')

    if not os.path.exists(target):
        os.mkdir(target, 0o755)

    for file_name in os.listdir(src):
        src_path = os.path.join(src, file_name)

        if os.path.isfile(src_path):
            callback(src_path, target)
        else:
            target_dir = os.path.join(target, file_name)
            map_dir(src_path, target_dir, callback)


def get_file_contents(file: str) -> str:
    f = open(file)

    try:
        return f.read()
    finally:
        f.close()


def put_file_contents(file: str, content: str, append: bool = False):
    dir = os.path.dirname(file)

    if not os.path.exists(dir):
        os.makedirs(dir, 0o755)

    if append:
        mode = 'a+'
    else:
        mode = 'w+'

    f = open(file, mode)

    try:
        f.write(content)
    finally:
        f.close()
