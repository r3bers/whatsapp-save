from os import listdir, environ, walk, path, makedirs
from time import sleep
from shutil import copy
from ntpath import basename
from datetime import datetime
from platform import system


class WhatsAppMonitor:
    def __init__(self):
        self.watch_path = '.'
        self.copy_path = 'WhatsApp.SAVE'
        current_system = system().lower()
        if current_system == 'windows':
            self.watch_path = path.join(environ['LOCALAPPDATA'], 'Packages')
            filtered = [folder for folder in listdir(self.watch_path) if "WhatsAppDesktop" in folder]
            if len(filtered) != 1:
                self.log('Error', ["Can't find WhatsAppDesktop folder in " + self.watch_path +
                                   " or it to many folders there. Resolve problem manually."])
                exit(1)
            self.watch_path = path.join(self.watch_path, filtered[0], 'LocalState', 'shared', 'transfers')
            # noinspection SpellCheckingInspection
            self.copy_path = path.join(environ['HOMEPATH'], self.copy_path)
        if current_system == 'linux':
            if 'ANDROID_ROOT' in environ:
                self.watch_path = path.join(environ['EXTERNAL_STORAGE'],
                                            'Android', 'media', 'com.whatsapp', 'WhatsApp', 'Media')
                self.copy_path = path.join(environ['EXTERNAL_STORAGE'], self.copy_path)
            else:
                self.log('Exit program', ['because it is Linux not Android'])
                exit(1)
        if not path.exists(self.copy_path):
            makedirs(self.copy_path)
        self.old_files = self.new_files = [path.join(dir_path, file) for (dir_path, dir_names, filenames) in
                                           walk(self.watch_path) for file in filenames]

    def compare_list(self):
        new_set = set(self.new_files)
        old_set = set(self.old_files)
        return new_set - old_set, old_set - new_set  # , new_set & old_set no need unchanged

    @staticmethod
    def log(log_operation, log_list):
        print(
            datetime.now().__str__() +
            ' - ' + log_operation + ': ' +
            ', '.join([basename(add_file) for add_file in log_list]))

    def run(self):
        while True:
            sleep(0.5)
            self.new_files = [path.join(dir_path, file) for (dir_path, dir_names, filenames) in
                              walk(self.watch_path) for file in filenames]
            added, deleted = self.compare_list()
            if added:
                self.log('Added', added)
                for file in added:
                    try:
                        copy(file, path.join(self.copy_path, basename(file)))
                    except IOError as e:
                        self.log('Copy Error', [e.msg])
            if deleted:
                self.log('Deleted', deleted)
            self.old_files = self.new_files.copy()


if __name__ == '__main__':
    WhatsAppMonitor().run()
