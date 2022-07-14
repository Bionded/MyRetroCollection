from _Old.Base.Backend.filesystem import getFS
import xmltodict
import logging
from _Old.Base.config_manager import Config_manager



def _pegasus_export(_source = '', _filepath = ''):
    return _source

class Importer():
    def __init__(self, fs=getFS(), config=Config_manager(), logger=logging.getLogger("__backend__")):
        self.exporters = dict()
        self.file_types = dict()
        self.logger = logger
        self.exporters["es_exporter"] = self._gamelist_import
        self.file_types['gamelist.xml'] = self._gamelist_import
        #self.exporters['pegasus_exporter'] = _pegasus_export
        #self.file_types['metadata.txt'] = _pegasus_export
        self.logging = logging.getLogger("__main__")
        self.supported_files = self.file_types.keys()
        self.filesystem = fs
        self.filesystem.import_files = self.supported_files


    def import_file(self,_filepath, _platform, _set_exporter = None):
        if not self.filesystem.file_exists(_filepath):
            self.logging.error(f"File '{_filepath}' not exist. Return None!")
            return None

        filename = self.filesystem.get_full_filename(_filepath)
        source_data = self.filesystem.get_content(_filepath)

        if _set_exporter:
            if _set_exporter in self.exporters.keys():
                import_val = self.exporters[_set_exporter](_source=source_data, _filepath=_filepath)
                self.filesystem.rename_file(_filepath,'.' + self.filesystem.get_full_filename(_filepath))
            else:
                self.logging.error(f"No Exporter with name '{_set_exporter}'!")
                return None

        if filename in self.file_types.keys():
            import_val = self.file_types[filename](_source=source_data, _filepath=_filepath)
            self.filesystem.rename_file(_filepath,'.' + self.filesystem.get_full_filename(_filepath))
        else:
            self.logging.error(f"No Exporter for filename '{filename}'!")
            return None
        return import_val

    def _gamelist_import(self, _source='', _filepath=''):
        gamelist_comparsion = {
            'path': 'path',
            'name': 'name',
            'desc': 'description',
            'image': 'screenshot_path',
            'video': 'video_path',
            'marquee': 'logo_path',
            'thumbnail': 'boxart_path',
            'rating': 'rating',
            'releasedate': 'release',
            'developer': 'developer',
            'publisher': 'publisher',
            'genre': 'genre',
            'players': 'players',
            'lang': 'language',
            'region': 'region',
        }
        temp_dict = xmltodict.parse(_source)['gameList']
        roms = []
        if 'game' in temp_dict.keys():
            for game in temp_dict['game']:
                temp_game_dict = dict()
                for key in game.keys():
                    if key in gamelist_comparsion.keys():
                        temp_game_dict[gamelist_comparsion[key]] = game[key]
                        if gamelist_comparsion[key] == 'path':
                            temp_game_dict[gamelist_comparsion[key]] = self.filesystem._path_join(
                                self.filesystem.get_dirname(_filepath),temp_game_dict[gamelist_comparsion[key]])
                        if gamelist_comparsion[key] == 'boxart_path':
                            temp_game_dict[gamelist_comparsion[key]] = self.filesystem._path_join(
                                self.filesystem.get_dirname(_filepath),temp_game_dict[gamelist_comparsion[key]])
                        if gamelist_comparsion[key] == 'screenshot_path':
                            temp_game_dict[gamelist_comparsion[key]] = self.filesystem._path_join(
                                self.filesystem.get_dirname(_filepath),temp_game_dict[gamelist_comparsion[key]])
                        if gamelist_comparsion[key] == 'video_path':
                            temp_game_dict[gamelist_comparsion[key]] = self.filesystem._path_join(
                                self.filesystem.get_dirname(_filepath),temp_game_dict[gamelist_comparsion[key]])
                        if gamelist_comparsion[key] == 'logo_path':
                            temp_game_dict[gamelist_comparsion[key]] = self.filesystem._path_join(
                                self.filesystem.get_dirname(_filepath),temp_game_dict[gamelist_comparsion[key]])
                        if gamelist_comparsion[key] == 'rating':
                            if float(temp_game_dict[gamelist_comparsion[key]]) <1:
                                temp_game_dict[gamelist_comparsion[key]] = float(temp_game_dict[gamelist_comparsion[key]]) * 10

                roms.append(temp_game_dict)
        return roms






