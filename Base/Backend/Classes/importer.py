import os

import xmltodict, json
from  os import path
import logging
from Base.Backend.Classes.platform import Rom, Platform



def _gamelist_export(_source = '',_filepath = ''):
    gamelist_comparsion = {
        'path': '_path',
        'name': '_full_name',
        'desc': '_description',
        'image': '_screenshot_path',
        'video': '_video_path',
        'marquee': '_logo',
        'thumbnail': '_boxart_path',
        'rating': '_rating',
        'releasedate': '_release',
        'developer': '_developer',
        'publisher': '_publisher',
        'genre': '_genre',
        'players': '_players',
        'lang': '_language',
        'region': '_region',
    }
    folder_path = os.path.dirname(_filepath)
    temp_dict = xmltodict.parse(_source)['gameList']
    roms = []
    if 'game' in temp_dict.keys():
        for game in temp_dict['game']:
            temp_game_dict = dict()
            temp_rom = Rom()
            for key in game.keys():
                if key in gamelist_comparsion.keys():
                    temp_game_dict[gamelist_comparsion[key]] = game[key]
            temp_rom.fromDict(temp_game_dict)
            temp_rom.setup(folder_path)
            temp_rom.man_edit = True
            roms.append(temp_rom)

    return roms


def _pegasus_export(_source = '',_filepath = ''):
    return _source

class Importer():
    def __init__(self):
        self.exporters = dict()
        self.file_types = dict()
        self.exporters["es_exporter"] = _gamelist_export
        self.file_types['gamelist.xml'] = _gamelist_export
        self.exporters['pegasus_exporter'] = _pegasus_export
        self.file_types['metadata.txt'] = _pegasus_export
        self.logging = logging.getLogger("__main__")



    def import_file(self,_filepath, _set_exporter = None):
        if not path.exists(_filepath):
            self.logging.error(f"File '{_filepath}' not exist. Return None!")
            return None

        filename = path.basename(_filepath)
        with open(_filepath, 'r') as file:
            source_data = file.read()

        if _set_exporter:
            if _set_exporter in self.exporters.keys():
                import_val = self.exporters[_set_exporter](source_data, _filepath)
            else:
                self.logging.error(f"No Exporter with name '{_set_exporter}'!")
                return None

        if filename in self.file_types.keys():
            import_val = self.file_types[filename](source_data, _filepath)
        else:
            self.logging.error(f"No Exporter for filename '{filename}'!")
            return None
        return import_val







