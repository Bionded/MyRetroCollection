import json
import hashlib

class Rom:
    def __init__(self, _id=-1, _name='', _description='', _md5sum='', _path='',
                 _platform='', _full_name='', _genre='', _rating='',_language='',
                 _developer='', _publisher='', _summary='', _release='', _players=0,
                 _boxart_path='', _screenshot_path='', _video_path='', _logo='', _region=''):
        self.id = _id
        self.name = _name
        self.description = _description
        self.md5sum = _md5sum
        self.path = _path
        self.full_path = _path
        self.platform = _platform
        self.full_name = _full_name
        self.genre = _genre
        self.rating = _rating
        self.language = _language
        self.developer = _developer
        self.publisher = _publisher
        self.summary = _summary
        self.release = _release
        self.players = _players
        self.boxart_path = _boxart_path
        self.screenshot_path = _screenshot_path
        self.video_path = _video_path
        self.logo = _logo
        self.region = _region
        self.man_edit = False
        self.scraped = False


    def md5(self):
        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.md5sum = hash_md5.hexdigest()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def fromJSON(self, _options=None):
        defaults = self.__dict__
        if _options is not None:
            for k, v in defaults.items():
                value = _options.get(k, v)
                defaults[k] = value

        self.__dict__.update(**defaults)


    #def fromJSON(self,_json):


