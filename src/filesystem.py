import os
import shutil

def copy_dir(src: str, target: str, remove_dest: bool = True):
    if not os.path.exists(src):
        raise Exception(f'Path "{src}" does not exist.')

    if not os.path.isdir(src):
        raise Exception(f'Path "{src}" is not a directory.')

    if remove_dest and os.path.exists(target):
        shutil.rmtree(target)

    if not os.path.exists(target):
        os.mkdir(target)

    for file_name in os.listdir(src):
        src_path = os.path.join(src, file_name)

        if os.path.isfile(src_path):
            shutil.copy(src_path, target)
        else:
            target_dir = os.path.join(target, file_name)
            copy_dir(src_path, target_dir, False)
