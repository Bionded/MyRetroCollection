import time
import json
from Base.Backend.storage import SQLStorage
from Base.Backend.importer import Importer
from Base.Backend.scanner import FileScanner
from Base.Backend.scanner import getFS
# from Base.Backend.scraper import Scraper
import logging
from Base.config_manager import Config_manager
import os
from queue import Queue
import threading
import re
import atexit


class Collector:
    def __init__(self, importer, scanner, config=Config_manager(),
                 storage=SQLStorage(), filesystem=getFS(), logger=logging.getLogger("__backend__")
                 ):
        self.config = config.set_section("Collector")
        self.logger = logger
        self.storage = storage
        self.importer = importer
        self.scanner = scanner
        self.filesystem = filesystem
        self.multithread = self.config.get_bool("multithread", True)
        self.supported_platforms = self.config.get("supported_platforms", []).strip('][').replace(' ', '').split(',')
        self.platforms_templates = self.load_templates()
        self.platforms = self.load_platforms()
        self.supported_import = self.importer.supported_files
        self.threads = {}
        if self.multithread:
            self.queues = {'main': Queue(),
                           'storage': Queue(),
                           'importer': Queue(),
                           'scanner': Queue(),
                           'scraper': Queue()}
        else:
            self.queues = Queue()

        self.start_threads()

    def start_threads(self):
        if self.multithread:
            for key in self.queues.keys():
                self.threads[key] = threading.Thread(target=self.solo_daemon, args=(key))
                self.threads[key].daemon = True
                self.threads[key].start()
        else:
            thread = threading.Thread(target=self.solo_daemon)
            thread.daemon = True
            thread.start()

    def solo_daemon(self):
        while True:
            time.sleep(1)
            job = self.queues.get()
            thread = threading.Thread(target=job['func'], args=job['args'])
            thread.start()
            thread.join()
            self.queues.task_done()

    def multi_thread_daemon(self, queue):
        while True:
            time.sleep(1)
            job = self.queues[queue].get()
            thread = threading.Thread(target=job['func'], args=job['args'])
            thread.start()
            thread.join()
            self.queues.task_done()

    ###########################################

    def load_platforms(self):
        temp_platforms = {}
        for splatform in self.supported_platforms:
            self.storage.add_platform(self.get_platform_template(splatform))

        exist_platforms = self.storage.get_all_platforms()
        for eplatform in exist_platforms:
            eplatform['extensions'] = eplatform['extensions'].strip('][').replace(' ', '').split(',')
            temp_platforms[eplatform['name']] = eplatform
        return temp_platforms

    def load_templates(self):
        with open(self.config.get("platform_templates", "DB/templates/platforms.json")) as json_file:
            return json.load(json_file)

    def add_to_queue(self, function, *args, queue='main'):
        if self.multithread:
            self.queues[queue].put({'func': function, 'args': args})
        else:
            self.queues.put({'func': function, 'args': args})

    def scan_platform(self, platform_name):
        self.add_to_queue(self._scan_platform, self.platforms[platform_name], queue='scanner')

    def test_scan(self, platform_name):
        ret_dict = self.scanner.scan_platform(self.platforms[platform_name])
        if 'imports' in ret_dict.keys():
            for import_file in ret_dict['imports']:
                self._import_exist_file(self.platforms[platform_name], import_file)



        if 'roms' in ret_dict.keys():
            newroms = []
            for rom in ret_dict['roms']:
                newrom = self._prepare_rom(rom=rom, platform=self.platforms[platform_name])
                if newrom:
                    newroms.append(newrom)
            if len(newroms) >0:
                self.storage.add_rom_list(ret_dict['roms'], update_exist=False)


    def _scan_platform(self, platform_name):
        ret_dict = self.scanner.scan_for_imports(self.platforms[platform_name])
        if 'imports' in ret_dict.keys():
            for import_file in ret_dict['imports']:
                self.add_to_queue(self._import_exist_file, self.platforms[platform_name], import_file, queue='importer')

    def _import_exist_file(self, platform: dict, path: str):
        ret_list = self.importer.import_file(path, platform)
        for rom in ret_list:
            newrom = self._prepare_rom(rom=rom, platform=platform)
            if newrom:
                rom = newrom
        self.storage.add_rom_list(ret_list, update_exist=True)

    def _prepare_rom(self, rom: dict, platform: dict):
        if 'path' not in rom.keys():
            return None
        if not self.filesystem.file_exists(rom['path']):
            return None
        if 'man_edit' in rom.keys():
            ################
            print('fdsafdsa')
            ################
        if 'name' not in rom.keys() or rom['name'] == '' or\
                '/' in rom['name'] or '[' in rom['name'] or\
                ']' in rom['name'] or '(' in rom['name'] or\
                ')' in rom['name']:
            newname = self.filesystem.get_filename(rom['path'])
            newname = newname.replace('/', '+').replace('!', ':')
            n = 1  # run at least once
            while n:
                newname, n = re.subn(r'\([^()]*\)', '', newname)
            n = 1  # run at least once
            while n:
                newname, n = re.subn(r'\[[^()]*\]', '', newname)
            newname = newname.strip()
            rom['name'] = newname.strip()
        if self.filesystem.get_filename(rom['path']) != rom['name'] or \
                not self.filesystem.get_dirname(rom['path']).endswith(platform['folder']):
            newpath = self.filesystem.move_file(rom['path'],
                                                self.filesystem._path_join(platform['folder'],
                                                                           rom['name'].replace(' - ', '-').replace(' ',
                                                                                                                   '_')))
            if newpath:
                rom['path'] = newpath
            else:
                return None
        if 'platform_id' not in rom.keys() or rom['platform_id'] <= 0:
            rom['platform_id'] = platform['id']
        if 'md5sum' not in rom.keys() or rom['md5sum'] == '' or \
                'sha1sum' not in rom.keys() or rom['sha1sum'] == '':
            hashes = self.filesystem.get_hashes(rom['path'])
            for key in hashes.keys():
                rom[key] = hashes[key]

        if 'boxart_path' in rom.keys():
            if not self.filesystem.file_exists(rom['boxart_path']):
                del rom['boxart_path']
            elif self.filesystem.get_filename(rom['boxart_path']) != rom['name'] or \
                    not self.filesystem.get_dirname(rom['boxart_path']).endswith('media/boxart_path'):
                newpath = self.filesystem.move_file(rom['boxart_path'],
                                                    self.filesystem._path_join(platform['folder'], 'media/boxart',
                                                                               rom['name']))
                if newpath:
                    rom['boxart_path'] = newpath

        if 'screenshot_path' in rom.keys():
            if not self.filesystem.file_exists(rom['screenshot_path']):
                del rom['screenshot_path']
            elif self.filesystem.get_filename(rom['screenshot_path']) != rom['name'] or \
                    not self.filesystem.get_dirname(rom['screenshot_path']).endswith('media/screenshot'):
                newpath = self.filesystem.move_file(rom['screenshot_path'],
                                                    self.filesystem._path_join(platform['folder'], 'media/screenshot',
                                                                               rom['name']))
                if newpath:
                    rom['screenshot_path'] = newpath

        if 'video_path' in rom.keys():
            if not self.filesystem.file_exists(rom['video_path']):
                del rom['video_path']
            elif  self.filesystem.get_filename(rom['video_path']) != rom['name'] or\
                not self.filesystem.get_dirname(rom['video_path']).endswith('media/video'):
                newpath = self.filesystem.move_file(rom['video_path'],
                                                    self.filesystem._path_join(platform['folder'], 'media/video',
                                                                               rom['name']))
                if newpath:
                    rom['video_path'] = newpath

        if 'logo_path' in rom.keys():
            if not self.filesystem.file_exists(rom['logo_path']):
                del rom['logo_path']
            elif self.filesystem.get_filename(rom['logo_path']) != rom['name'] or\
                not self.filesystem.get_dirname(rom['logo_path']).endswith('media/logo'):
                newpath = self.filesystem.move_file(rom['logo_path'],
                                                    self.filesystem._path_join(platform['folder'], 'media/logo',
                                                                               rom['name']))
                if newpath:
                    rom['logo_path'] = newpath

        if 'man_edit' not in rom.keys():
            rom['man_edit'] = False
        if 'exist' not in rom.keys():
            rom['exist'] = False
        if 'scraped' not in rom.keys():
            rom['scraped'] = False
        return rom

    # def analyze_rom(self,filedict: dict):

    def get_platform_template(self, name: str):
        if name in self.platforms_templates.keys():
            return self.platforms_templates[name]
        else:
            return {
                "name": name,
                "man_edit": False
            }

    def close_platform(self):
        for platform in self.platforms.values():
            platform.close()

    def __scan_folder(self, folder):
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]

    def __scan_platform(self, platform_name: str):
        with self.platforms[platform_name].get_platform() as pltfrm:
            path_to_platform = os.path.join(self.base_rom_folder, pltfrm.folder)

    # def start_scan(self, _folder='/Volumes/Bionded/Roms/gba'):
    #     self.queue.put({'func': self.__scan_folder, 'args': (_folder,), 'name': f'Scan {_folder}'})
    #
    # def __scan_folder(self, _folder):
    #     for f in listdir(_folder):
    #         if path.isfile(path.join(_folder, f)):
    #             self.files_dict[f] = self.md5(path.join(_folder, f))
    #
    #     return "IAM FINISH!"

    def send(self, _message):
        self.logger.info(f"Message: {_message}")
        return f"Message: {_message}"
