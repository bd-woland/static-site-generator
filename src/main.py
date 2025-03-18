from filesystem import (copy_dir)
from functions import (generate_pages_recursive)
import os, shutil, sys

static_dir = './static'
public_dir = './docs'
content_dir = './content'
template_path = './template.html'

def main():
    if len(sys.argv) < 2:
        basepath = '/'
    else:
        basepath = sys.argv[1]

    if os.path.exists(public_dir):
        print('Deleting public directory...')
        shutil.rmtree(public_dir)

    print('Copying static files to public directory...')
    copy_dir(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir, basepath)


main()
