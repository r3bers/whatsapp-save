from os import listdir, environ, walk, path, makedirs
from time import sleep
from shutil import copy
from ntpath import basename
from datetime import datetime


def compare_list(old, new):
    new_set = set(new)
    old_set = set(old)
    return new_set - old_set, old_set - new_set, new_set & old_set


if __name__ == '__main__':
    save_dir = 'WhatsApp.SAVE'
    watch_path = path.join(environ['LOCALAPPDATA'], 'Packages')
    filtered = [folder for folder in listdir(watch_path) if "WhatsAppDesktop" in folder]
    if len(filtered) != 1:
        print("Can't find WhatsAppDesktop folder in " + watch_path +
              " or it to many folders there. Resolve problem manually.")
        exit(1)

    watch_path = path.join(watch_path, filtered[0], 'LocalState', 'shared', 'transfers')
    # noinspection SpellCheckingInspection
    copy_path = path.join(environ['HOMEPATH'], save_dir)
    if not path.exists(copy_path):
        makedirs(copy_path)
    old_files = [path.join(dir_path, f) for (dir_path, dir_names, filenames) in walk(watch_path) for f in filenames]
    while True:
        sleep(0.5)
        new_files = [path.join(dir_path, f) for (dir_path, dir_names, filenames) in walk(watch_path) for f in filenames]
        added, deleted, unchanged = compare_list(old_files, new_files)
        if added:
            print(datetime.now().__str__() + ' - Added: ' + ', '.join([basename(add_file) for add_file in added]))
            try:
                [copy(each_file, path.join(copy_path, basename(each_file))) for each_file in added]
            # include the file to be deleted in array
            except IOError as e:
                print('Copy Error: ', end='')
                print(e.msg)
                sleep(0.5)
        if deleted:
            print(datetime.now().__str__() + '  - Deleted: ' + ', '.join([basename(del_file) for del_file in deleted]))
        # if unchanged:
        # print('.', end='')
        old_files = new_files.copy()
