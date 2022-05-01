import os

import xmltodict, json
from  os import path
import logging
from Base.Backend.Classes import rom, collection



def _gamelist_export(_source = '',_filepath = ''):
    gamelist_comparsion = {
        '@id': 'id',
        'id': 'id',
        'path': 'path',
        'name': 'full_name',
        'desc': 'description',
        'image': 'screenshot_path',
        'video': 'video_path',
        'marquee': 'logo',
        'thumbnail': 'boxart_path',
        'rating':'rating',
        'releasedate':'release',
        'developer':'developer',
        'publisher':'publisher',
        'genre':'genre',
        'players':'players',
        'lang':'language',
        'region':'region',
    }
    folder_path = os.path.dirname(_filepath)
    temp_dict = xmltodict.parse(_source)['gameList']
    temp_collection = collection.Collection()
    roms = []
    if 'provider' in temp_dict.keys():
        temp_collection.name = temp_dict['provider']['system']
    if 'game' in temp_dict.keys():
        for game in temp_dict['game']:
            temp_game_dict = dict()
            temp_rom = rom.Rom()
            for key in game.keys():
                if key in gamelist_comparsion.keys():
                    temp_game_dict[gamelist_comparsion[key]] = game[key]
            temp_game_dict['platform'] = temp_collection.name
            temp_game_dict['full_path'] = os.path.join(folder_path, temp_game_dict['path'])
            temp_rom.fromJSON(temp_game_dict)
            temp_rom.md5()
            roms.append(temp_rom)


    return {'collection':temp_collection,'roms': roms}


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







