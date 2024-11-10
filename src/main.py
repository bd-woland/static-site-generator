from filesystem import (copy_dir)
from functions import (generate_pages_recursive)
import os, shutil

static_dir = './static'
public_dir = './public'
content_dir = './content'
template_path = './template.html'

def main():
    if os.path.exists(public_dir):
        print('Deleting public directory...')
        shutil.rmtree(public_dir)

    print('Copying static files to public directory...')
    copy_dir(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir)


main()
