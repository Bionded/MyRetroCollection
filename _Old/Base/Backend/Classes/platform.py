import hashlib
import os.path


class Rom:
    def __init__(self, _name=None, _description=None, _md5sum=None, _sha1sum=None, _path='',
                 _full_name=None, _genre=None, _rating=None, _language=None,
                 _developer=None, _publisher=None, _summary='', _release=None, _players=None,
                 _boxart_path=None, _screenshot_path=None, _video_path=None, _logo='', _region=None):
        self._name = _name
        self._description = _description
        self._md5sum = _md5sum
        self._sha1sum = _sha1sum
        self._path = _path
        self._full_name = _full_name
        self._genre = _genre
        self._rating = _rating
        self._language = _language
        self._developer = _developer
        self._publisher = _publisher
        self._release = _release
        self._players = _players
        self._boxart_path = _boxart_path
        self._screenshot_path = _screenshot_path
        self._video_path = _video_path
        self._logo = _logo
        self._region = _region
        self._man_edit = False
        self._scraped = False
        self._exists = True

    def delete_files(self, base_folder=''):
        os.remove(os.path.join(base_folder, self.path))
        os.remove(os.path.join(base_folder, self.boxart_path))
        os.remove(os.path.join(base_folder, self.screenshot_path))
        os.remove(os.path.join(base_folder, self.video_path))

    def setup(self, base_folder=''):
        full_path = os.path.join(base_folder, self._path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            self.exists = True
        else:
            self.exists = False

        if self.exists:
            self.get_hash(full_path)

    def get_hash(self, path=''):
        if path.endswith(self._path):
            full_path = path
        else:
            full_path = os.path.join(path, self._path)
        hash_md5 = hashlib.md5()
        hash_sha1 = hashlib.sha1()
        if os.path.exists(self._path):
            path_to_rom = self._path
        elif (os.path.exists(full_path)):
            path_to_rom = full_path
        else:
            path_to_rom = None
        if path_to_rom:
            with open(path_to_rom, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                    hash_sha1.update(chunk)
            self.md5sum = hash_md5.hexdigest()
            self.sha1sum = hash_sha1.hexdigest()
            self.hashsum = self.combine_hash()

    def combine_hash(self):
        if self.md5sum and self.sha1sum:
            return self.md5sum+self.sha1sum
        else:
            return None

    def fromDict(self, _options: dict):
        defaults = self.__dict__
        if _options is not None:
            for k, v in defaults.items():
                value = _options.get(k, v)
                if value:
                    defaults[k] = value

        self.__dict__.update(**defaults)
        return self

    def keys(self):
        return self.__dict__.keys()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        self._description = new_description

    @property
    def md5sum(self) -> str:
        return self._md5sum

    @md5sum.setter
    def md5sum(self, new_md5sum: str):
        self._md5sum = new_md5sum

    @property
    def sha1sum(self) -> str:
        return self._sha1sum

    @sha1sum.setter
    def sha1sum(self, new_sha1sum: str):
        self._sha1sum = new_sha1sum

    @property
    def hashsum(self) -> str:
        return self._hashsum

    @hashsum.setter
    def hashsum(self, new_hashsum: str):
        self._hashsum = new_hashsum

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, new_path: str):
        self._path = new_path

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, new_full_name: str):
        self._full_name = new_full_name

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, new_genre: str):
        self._genre = new_genre

    @property
    def rating(self) -> str:
        return self._rating

    @rating.setter
    def rating(self, new_rating: str):
        self._rating = new_rating

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        self._language = new_language

    @property
    def developer(self) -> str:
        return self._developer

    @developer.setter
    def developer(self, new_developer: str):
        self._developer = new_developer

    @property
    def publisher(self) -> str:
        return self._publisher

    @publisher.setter
    def publisher(self, new_publisher: str):
        self._publisher = new_publisher

    @property
    def release(self) -> str:
        return self._release

    @release.setter
    def release(self, new_release: str):
        self._release = new_release

    @property
    def players(self) -> int:
        return self._players

    @players.setter
    def players(self, new_players: int):
        self._players = new_players

    @property
    def boxart_path(self) -> str:
        return self._boxart_path

    @boxart_path.setter
    def boxart_path(self, new_boxart_path: str):
        self._boxart_path = new_boxart_path

    @property
    def screenshot_path(self) -> str:
        return self._screenshot_path

    @screenshot_path.setter
    def screenshot_path(self, new_screenshot_path: str):
        self._screenshot_path = new_screenshot_path

    @property
    def video_path(self) -> str:
        return self._video_path

    @video_path.setter
    def video_path(self, new_video_path: str):
        self._video_path = new_video_path

    @property
    def logo(self) -> str:
        return self._logo

    @logo.setter
    def logo(self, new_logo: str):
        self._logo = new_logo

    @property
    def region(self) -> str:
        return self._region

    @region.setter
    def region(self, new_region: str):
        self._region = new_region

    @property
    def man_edit(self) -> bool:
        return self._man_edit

    @man_edit.setter
    def man_edit(self, new_man_edit: bool):
        self._man_edit = new_man_edit

    @property
    def scraped(self) -> bool:
        return self._scraped

    @scraped.setter
    def scraped(self, new_scraped: bool):
        self._scraped = new_scraped

    @property
    def exists(self) -> bool:
        return self._exists

    @exists.setter
    def exists(self, new_exists: bool):
        self._exists = new_exists


class Platform:
    def __init__(self, _name=None, _description=None, _full_name=None,
                 _developer=None, _release=None, _extensions=None):
        self._name = _name
        self._description = _description
        self._full_name = _full_name
        self._developer = _developer
        self._release = _release
        self._extensions = _extensions
        self._man_edit = False

    def __eq__(self, other):
        if isinstance(other, Platform):
            return (self._name == other._name and
                    self._description == other._description and
                    self._full_name == other._full_name and
                    self._developer == other._developer and
                    self._release == other._release and
                    self._extensions == other._extensions)
        return NotImplemented

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, new_full_name):
        self._full_name = new_full_name

    @property
    def developer(self):
        return self._developer

    @developer.setter
    def developer(self, new_developer):
        self._developer = new_developer

    @property
    def release(self):
        return self._release

    @release.setter
    def release(self, new_release):
        self._release = new_release

    @property
    def extensions(self) -> str:
        return self._extensions

    @extensions.setter
    def extensions(self, new_extensions: str):
        self._extensions = new_extensions

    @property
    def man_edit(self) -> bool:
        return self._man_edit

    @man_edit.setter
    def man_edit(self, new_man_edit: bool):
        self._man_edit = new_man_edit

    def fromDict(self, _options: dict):
        defaults = self.__dict__
        if _options is not None:
            for k, v in defaults.items():
                value = _options.get(k, v)
                if value:
                    defaults[k] = value

        self.__dict__.update(**defaults)
        return self

    def keys(self):
        return self.__dict__.keys()
