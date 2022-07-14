import json
from _Old.Base.Backend.storage import SQLStorage
from _Old.Base.Backend.importer import Importer
from _Old.Base.Backend.scanner import FileScanner
from _Old.Base.Backend.scanner import getFS
# from Base.Backend.scraper import Scraper
import logging
from _Old.Base.config_manager import Config_manager
import re


class Collector:
    def __init__(self, importer=Importer(), scanner=FileScanner(), config=Config_manager(),
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

    ###########################################

    def load_platforms(self):
        temp_platforms = {}

        exist_platforms = self.storage.get_all_platforms()
        test = i['name'] for i in exist_platforms
        for splatform in self.supported_platforms:
            if splatform not in test:
                self.storage.add_platform(self.get_platform_template(splatform))

        for eplatform in exist_platforms:
            eplatform['extensions'] = eplatform['extensions'].strip('][').replace(' ', '').split(',')
            temp_platforms[eplatform['name']] = eplatform
        return temp_platforms

    def load_templates(self):
        with open(self.config.get("platform_templates", "DB/templates/platforms.json")) as json_file:
            return json.load(json_file)


    def _import_exist_file(self, platform: dict, path: str):
        ret_list = self.importer.import_file(path, platform)
        for rom in ret_list:
            newrom = self._prepare_rom(rom=rom, platform=platform)
            if newrom:
                self.storage.add_rom(newrom, True)

    def _add_rom(self, rom: dict):
        self.storage.add_rom(rom, update_exist=True)

    def _prepare_rom(self, rom: dict, platform: dict):
        if 'path' not in rom.keys():
            return None
        if not self.filesystem.file_exists(rom['path']):
            return None
        if 'man_edit' in rom.keys():
            ################
            print('fdsafdsa')
            ################
        if 'name' not in rom.keys() or rom['name'] == '' or \
                '/' in rom['name'] or '[' in rom['name'] or \
                ']' in rom['name'] or '(' in rom['name'] or \
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
            elif self.filesystem.get_filename(rom['video_path']) != rom['name'] or \
                    not self.filesystem.get_dirname(rom['video_path']).endswith('media/video'):
                newpath = self.filesystem.move_file(rom['video_path'],
                                                    self.filesystem._path_join(platform['folder'], 'media/video',
                                                                               rom['name']))
                if newpath:
                    rom['video_path'] = newpath

        if 'logo_path' in rom.keys():
            if not self.filesystem.file_exists(rom['logo_path']):
                del rom['logo_path']
            elif self.filesystem.get_filename(rom['logo_path']) != rom['name'] or \
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

    def get_platform_template(self, name: str):
        if name in self.platforms_templates.keys():
            return self.platforms_templates[name]
        else:
            return {
                "name": name,
                "man_edit": False
            }
