import json
from tinydb import TinyDB, Query,table
from Base.Backend.Classes import rom

class Base_platoform:
    def __init__(self, _id=-1, _name='', _description='', _folder='', _full_name='',
                 _developer='', _summary='', _release='', _extensions=''):
        self.id = _id
        self.name = _name
        self.description = _description
        self.folder = _folder
        self.full_name = _full_name
        self.developer = _developer
        self.summary = _summary
        self.release = _release
        self.extensions = _extensions


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def fromJSON(self, _options):
        defaults = {"id": "-1"}
        if _options is not None:
            for k, v in defaults.items():
                value = _options.get(k, v)
                defaults[k] = value

        self.__dict__.update(**defaults)

class tiny_table_platform:
    def __init__(self, _db_path=''):
        self.db_path = _db_path
        self.DB = TinyDB(_db_path)
        self.platform_confs = TinyDB.table('platform')
        self.roms_table = TinyDB.table('roms')

