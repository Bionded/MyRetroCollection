from core.utils.types import *
import hashlib
import zlib
import os

class fs_manager:
    def __init__(self, core):
        self.name = "fs_manager"
        self.version = "0.0.1"
        self._core = core
        self.config_manager = self._core.config_manager
        self.plugin_manager = self._core.plugin_manager
        self.logs_manager = self._core.logs_manager
        self.logger = self.logs_manager.getLogger(self)
        self.config = self.config_manager.getConfig(self)
        self.fs_driver = self.config.getValue('fs_driver', 'default')


    def get_fs_driver(self):
        if self.fs_driver == 'default':
            self.logger.info(self, "Using default fs driver")
            return default_fs(self)
        driver = self.plugin_manager.doCommand(self, 'get_fs_driver', self.fs_driver)
        if driver:
            self.logger.info(self, f"Using fs driver {self.fs_driver}")
            return driver
        else:
            self.logger.error(self, f"fs driver {self.fs_driver} not found use default")
            return default_fs(self)

    def set_fs_driver_name(self, driver):
        if self.plugin_manager.getPlugin(driver):
            self.config.setValue('fs_driver', driver)
            self.config_manager.saveConfig(self)
            self.logger.info(self, f"fs driver set to {driver}")
            return True
        else:
            self.logger.error(self, f"fs driver {driver} not found or disabled, driver set to {self.fs_driver}")
            return False

    def get_fs_driver_name(self):
        return self.fs_driver

class default_fs:
    def __init__(self, fs_manager):
        self.name = "default_fs"
        self._fs_manager = fs_manager
        self.version = self._fs_manager.version
        self.config = self._fs_manager.config_manager.getConfig(self)
        self.logger = self._fs_manager.logs_manager.getLogger(self)

    def _file_by_path(self, path: str):
        if os.path.isfile(path):
            return self.get_file_info(path)
        else:
            return None
    def get_file(self, file: FileClass):
        if file.fs_driver == 'default':
            return self._file_by_path(file.path)
        else:
            self.logger.warning(self, f"fs driver {file.fs_driver} not active now, set different fs driver to get this file")
            return None

    def calc_hash(self, file: FileClass, force: bool = False):
        if file.md5 is None or force:
            with open(file.path, 'rb') as f:
                file.md5 = hashlib.md5(f.read()).hexdigest()
        if file.sha1 is None or force:
            with open(file.path, 'rb') as f:
                file.sha1 = hashlib.sha1(f.read()).hexdigest()
        if file.crc is None or force:
            with open(file.path, 'rb') as f:
                file.crc = zlib.crc32(f.read())
        return file

    def get_file_info(self, file: str):
        temp = FileClass(None, file, os.path.basename(file), os.path.getsize(file), os.path.splitext(file)[1],
                         None, None, None, 'default')
        return self.calc_hash(temp, force=True)
    def get_file_list(self, path:str, recursive:bool=False, info:bool=False):
        files = []
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                files.append(os.path.join(path, file))
            elif os.path.isdir(os.path.join(path, file)) and recursive:
                files += self.get_file_list(os.path.join(path, file), recursive)
        if info:
            temp = []
            for file in files:
                temp.append(self.get_file_info(file))
            files = temp
        return files

    def get_file_list_with_ext(self, path:str, ext:list, recursive:bool=False, info:bool=False):
        files = []
        new_ext = []
        for extension in ext:
            if not extension.startswith('.'):
                new_ext.append('.' + extension)
            else:
                new_ext.append(extension)
        ext = new_ext
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and os.path.splitext(file)[1] in ext:
                files.append(os.path.join(path, file))
            elif os.path.isdir(os.path.join(path, file)) and recursive:
                files += self.get_file_list_with_ext(os.path.join(path, file), ext, recursive)
        if info:
            temp = []
            for file in files:
                temp.append(self.get_file_info(file))
            files = temp
        return files



