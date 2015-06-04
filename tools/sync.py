# coding=utf-8
__author__ = 'gongxingfa'

# It's used to sync files on more than two directory.
# Used python sync.py /Users/test/A /Users/test/B


import os


def flat_files(root, filter_func=None):
    real_filter_func = filter_func if filter_func else lambda x: True
    directories = os.walk(root)
    for directory_info in directories:
        direct = directory_info[0]
        files = directory_info[-1]
        for f in files:
            file_path = os.path.join(direct, f)
            if real_filter_func(file_path):
                yield file_path


def mkdirs(path):
    flat_dirs = path.split('/')
    flat_dirs = [d for d in flat_dirs if d]
    flat_dirs = flat_dirs[::-1]
    directory = os.path.join('/', flat_dirs.pop())
    while flat_dirs:
        if not os.path.exists(directory):
            os.mkdir(directory)
        directory = os.path.join(directory, flat_dirs.pop())
    if not os.path.exists(directory):
        os.mkdir(directory)


def copy(src, dest):
    src_file = open(src, 'rb')
    dest_file = open(dest, 'wb')
    for line in src_file:
        dest_file.write(line)
    dest_file.close()


def relate_path(dirs, absolute_path):
    path = None
    for d in dirs:
        if absolute_path.startswith(d):
            path = absolute_path.replace(d, '')
            if path.startswith('/'):
                path = path[1:]
            return path


def sync_file(source_file, dirs):
    rp = relate_path(dirs, source_file)
    for d in dirs:
        dest_file = os.path.join(d, rp)
        if not os.path.exists(dest_file):
            real_directory = dest_file[:dest_file.rfind('/')]
            mkdirs(real_directory)
            copy(source_file, dest_file)


def sync(dir1, dir2, *dirs):
    all_dirs = [d for d in dirs]
    all_dirs.insert(0, dir2)
    all_dirs.insert(0, dir1)
    for d in all_dirs:
        for f in flat_files(d):
            sync_file(f, all_dirs)
            print 'Sync ', f


if __name__ == '__main__':
    import sys

    argv = sys.argv[1:]
    sync(sys.argv[0], sys.argv[1], *argv[2:])


