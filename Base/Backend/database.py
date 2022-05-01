from pysondb import db


class json_db:
    def __init__(self, _path_to_db=''):
        self.db_path = _path_to_db
        self.db = db.getDb(self.db_path)