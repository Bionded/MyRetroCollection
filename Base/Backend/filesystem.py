import os
from typing import Any, Callable, Dict, List, Union, Pattern, Type
from Base.config_manager import Config_manager
import logging
import hashlib
import shutil

# def getFS(config=Config_manager(), logger=logging.getLogger("__backend__")):
#     config = config.set_section('Filesystem')
#     fs_type = config.get("type", 'native')
#
#     return allFS[fs_type](config=config, logger=logger)


class getFS:
    def __init__(self, config=Config_manager(), logger=logging.getLogger("__backend__")):
        self.config = config.set_section('Filesystem')
        self.logger = logger
        self.base_folder = os.path.abspath(self.config.get("base_folder", '/Volumes/Bionded/Roms'))
        self._import_files = list()


    @property
    def import_files(self):
        return self._import_files

    @import_files.setter
    def import_files(self, files:list):
        self._import_files = files

    def _path_join(self, *kwargs):
        os.chdir(self.base_folder)
        return os.path.abspath(os.path.join(*kwargs))

    def get_all_files(self, folder,extensions=None):
        os.chdir(self.base_folder)
        workdir = self._path_join(self.base_folder, folder)
        roms = []
        import_files = []
        for root, dirnames, filenames in os.walk(workdir):
            for filename in filenames:
                if filename in self._import_files:
                    import_files.append(self._path_join(root, filename))
                elif extensions:
                    if os.path.splitext(filename)[1] in extensions:
                        temprom={'path': self._path_join(root, filename)}
                        roms.append(temprom)
        if len(import_files)>0:
            return {'roms': roms, 'imports': import_files}
        else:
            return {'roms': roms}

    def file_exists(self, path):
        os.chdir(self.base_folder)
        if os.path.exists(path) and os.path.isfile(path):
            return True
        else:
            return False

    def folder_exists(self, path, create=True):
        os.chdir(self.base_folder)
        if os.path.exists(path) and os.path.isdir(path):
            return True
        elif create:
            os.makedirs(path)
            return True
        else:
            return False

    def get_hashes(self, path):
        os.chdir(self.base_folder)
        if self.file_exists(path):
            tempdict = {}
            hash_md5 = hashlib.md5()
            hash_sha1 = hashlib.sha1()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                    hash_sha1.update(chunk)
            tempdict['md5sum'] = hash_md5.hexdigest()
            tempdict['sha1sum'] = hash_sha1.hexdigest()

        return tempdict

    def get_full_filename(self, path):
        os.chdir(self.base_folder)
        return os.path.basename(path)

    def get_file_ext(self,path):
        os.chdir(self.base_folder)
        return os.path.splitext(os.path.basename(path))[1]
    def get_filename(self, path):
        os.chdir(self.base_folder)
        return os.path.splitext(os.path.basename(path))[0]

    def get_dirname(self,path):
        os.chdir(self.base_folder)
        return os.path.dirname(path)

    def get_content(self, path):
        os.chdir(self.base_folder)
        if self.file_exists(path):
            with open(path, 'r') as file:
                data = file.read()
            return data
        else:
            return None

    def move_file(self,fpath, tpath):
        os.chdir(self.base_folder)
        newext = None
        if self.get_file_ext(fpath) !=self.get_file_ext(tpath):
            newext = self.get_file_ext(fpath)
        if not fpath.startswith('/'):
            fpath = os.path.abspath(fpath)
        if not tpath.startswith('/'):
            tpath = os.path.abspath(tpath)
        if newext:
            dir=os.path.dirname(tpath)
            filename= self.get_filename(tpath) +newext
            tpath = self._path_join(dir,filename)
        if self.file_exists(fpath) and self.folder_exists(os.path.dirname(tpath), create=True):
            shutil.move(fpath,tpath)
        else:
            return None
        return tpath








# allFS = {'native': Native}