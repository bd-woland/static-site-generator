from filesystem import (copy_dir)
from functions import (generate_page)
import os, shutil

static_dir = './static'
public_dir = './public'

def main():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_dir(static_dir, public_dir)
    generate_page('./content/index.md', './template.html', os.path.join(public_dir, 'index.html'))


main()
