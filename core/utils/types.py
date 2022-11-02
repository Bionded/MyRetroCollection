from typing import List, Dict


class FileClass:
    id: int = None
    path: str = None
    name: str = None
    size: int = None
    extension: str = None
    md5: str = None
    sha1: str = None
    crc: str = None
    fs_driver: str = None
    existing: bool = False

    def __init__(self, file_id: int = None, file_path: str = None, file_name: str = None, file_size: int = None,
                 file_extension: str = None, file_md5: str = None, file_sha1: str = None, file_crc: str = None,
                 file_driver: str = None, file_existing: bool = False):
        if type(file_id) is int:
            self.id = file_id
        elif file_id is None:
            pass
        else:
            raise TypeError("file_id must be int")
        if type(file_path) is str:
            self.path = file_path
        else:
            raise TypeError("file_path must be str")
        if type(file_name) is str:
            self.name = file_name
        else:
            raise TypeError("file_name must be str")
        if type(file_size) is int:
            self.size = file_size
        else:
            raise TypeError("file_size must be int")
        if type(file_extension) is str:
            if file_extension.startswith('.'):
                self.extension = file_extension
            else:
                self.extension = '.' + file_extension
        else:
            raise TypeError("file_extension must be str")
        if type(file_md5) is str:
            self.md5 = file_md5
        elif file_md5 is None:
            pass
        else:
            raise TypeError("file_md5 must be str")
        if type(file_sha1) is str:
            self.sha1 = file_sha1
        elif file_sha1 is None:
            pass
        else:
            raise TypeError("file_sha1 must be str")
        if type(file_crc) is int:
            self.crc = file_crc
        elif file_crc is None:
            pass
        else:
            raise TypeError("file_crc must be int")
        if type(file_driver) is str:
            self.fs_driver = file_driver
        else:
            raise TypeError("file_driver must be str")
        if type(file_existing) is bool:
            self.existing = file_existing
        else:
            raise TypeError("file_existing must be bool")

    def to_dict(self):
        return self.__dict__


class LocaleClass:
    id: int = None
    _strings: Dict = {}
    default_language: str = 'en'
    _allowed_langs = ['en', 'fr', 'de', 'es', 'it', 'ua', 'ja', 'ko', 'pt', 'ru', 'zh']

    def __init__(self, locale_id: int = None, locale_strings: dict = None, locale_default_language: str = 'en'):
        if type(locale_id) is int:
            self.id = locale_id
        elif locale_id is None:
            pass
        else:
            raise TypeError("locale_id must be int")

        if type(locale_strings) is dict:
            self._strings = locale_strings
        elif locale_strings is None:
            pass
        else:
            raise TypeError("locale_strings must be dict")

        self.set_default_locale(locale_default_language)

        if self._strings == {}:
            self._strings = {self.default_language: ''}

    def __repr__(self):
        return f"{self.id}: {self._strings[self.default_language]}"

    def set_locale(self, language, string):
        self._strings[language] = string

    def get_locale(self, language):
        return self._strings[language]

    def get_default_locale(self):
        return self._strings[self.default_language]

    def get_all_locales(self):
        return self._strings.keys()

    def set_default_locale(self, language):
        if language in self._strings.keys():
            self.default_language = language
        elif language in self._allowed_langs:
            self._strings[language] = ''
            self.default_language = language
        elif language is None:
            pass
        else:
            raise ValueError("language must be one of the following: " + ', '.join(self._strings.keys()))

    def to_dict(self):
        return {'id': self.id, 'strings': self._strings, 'default_language': self.default_language}


class RomClass(FileClass):
    beta: bool = False
    demo: bool = False
    proto: bool = False
    trad: bool = False
    hack: bool = False
    unl: bool = False
    alt: bool = False
    best: bool = False
    netplay: bool = False

    def __init__(self, rom_id: int = None, rom_path: str = None, rom_name: str = None, rom_size: int = None,
                 rom_extension: str = None, rom_md5: str = None, rom_sha1: str = None, rom_crc: str = None,
                 rom_file_driver: str = None, is_beta: bool = False, is_demo: bool = False, is_proto: bool = False,
                 is_trad: bool = False, is_hack: bool = False, is_unl: bool = False, is_alt: bool = False,
                 is_best: bool = False, is_netplay: bool = False, is_existing: bool = False):
        super().__init__(rom_id, rom_path, rom_name, rom_size, rom_extension,
                         rom_md5, rom_sha1, rom_crc, rom_file_driver, is_existing)
        if type(is_beta) is bool:
            self.beta = is_beta
        else:
            raise TypeError("is_beta must be bool")
        if type(is_demo) is bool:
            self.demo = is_demo
        else:
            raise TypeError("is_demo must be bool")
        if type(is_proto) is bool:
            self.proto = is_proto
        else:
            raise TypeError("is_proto must be bool")
        if type(is_trad) is bool:
            self.trad = is_trad
        else:
            raise TypeError("is_trad must be bool")
        if type(is_hack) is bool:
            self.hack = is_hack
        else:
            raise TypeError("is_hack must be bool")
        if type(is_unl) is bool:
            self.unl = is_unl
        else:
            raise TypeError("is_unl must be bool")
        if type(is_alt) is bool:
            self.alt = is_alt
        else:
            raise TypeError("is_alt must be bool")
        if type(is_best) is bool:
            self.best = is_best
        else:
            raise TypeError("is_best must be bool")
        if type(is_netplay) is bool:
            self.netplay = is_netplay
        else:
            raise TypeError("is_netplay must be bool")


class MediaClass(FileClass):
    media_format: str = None
    type: str = None

    def __init__(self, media_id: int = None, media_path: str = None, media_name: str = None, media_size: int = None,
                 media_extension: str = None, media_md5: str = None, media_sha1: str = None, media_crc: str = None,
                 media_file_driver: str = None, media_format: str = None, media_type: str = None,
                 is_existing: bool = False):
        super().__init__(media_id, media_path, media_name, media_size, media_extension,
                         media_md5, media_sha1, media_crc, media_file_driver, is_existing)
        if type(media_format) is str:
            self.media_format = media_format
        else:
            raise TypeError("media_format must be str")
        if type(media_type) is str:
            self.type = media_type
        else:
            raise TypeError("media_type must be str")


class GenreClass:
    id: int = None
    name: str = None
    _media: List[MediaClass] = []

    def __init__(self, genre_id: int = None, genre_name: str = None, genre_medias: List[MediaClass] = None):
        if type(genre_id) is int:
            self.id = genre_id
        else:
            raise TypeError("genre_id must be int")
        if type(genre_name) is str:
            self.name = genre_name
        else:
            raise TypeError("genre_name must be str")
        self.media = genre_medias

    def __repr__(self):
        return f"{self.name}"

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, medias: List[MediaClass]):
        if type(medias) is List[MediaClass]:
            self._media = medias
        elif medias is None:
            pass
        else:
            raise TypeError("medias must be list of media_class")

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'media': [media.to_dict() for media in self.media]}


class CompanyClass:
    id: int = None
    name: str = None
    _description: LocaleClass = None
    _media: List[MediaClass] = None

    def __init__(self, company_id: int = None, company_name: str = None, company_description: LocaleClass = None,
                 company_medias: List[MediaClass] = None):
        if type(company_id) is int:
            self.id = company_id
        else:
            raise TypeError("company_id must be int")
        if type(company_name) is str:
            self.name = company_name
        else:
            raise TypeError("company_name must be str")
        self.description = company_description
        self.media = company_medias

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: LocaleClass):
        if type(description) is LocaleClass:
            self._description = description
        elif description is None:
            pass
        else:
            raise TypeError("description must be locale")

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, medias: List[MediaClass]):
        if type(medias) is List[MediaClass]:
            self._media = medias
        elif medias is None:
            pass
        else:
            raise TypeError("medias must be list of media_class")

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description.to_dict(),
                'media': [media.to_dict() for media in self.media]}


class SystemClass:
    id: int = None
    name: str = None
    path: str = None
    _company: CompanyClass = None
    short_name: str = None
    type: str = None
    _description: LocaleClass = None
    _media: List[MediaClass] = None
    _extensions: List[str] = []
    scraped: bool = False
    manual_edit: bool = False

    def __init__(self, system_id: int = None, system_name: str = None, system_path: str = None,
                    system_company: CompanyClass = None, system_short_name: str = None, system_type: str = None,
                    system_description: LocaleClass = None, system_medias: List[MediaClass] = None,
                    system_extensions: List[str] = None, system_scraped: bool = False, system_manual_edit: bool = False):
        if type(system_id) is int:
            self.id = system_id
        else:
            raise TypeError("system_id must be int")
        if type(system_name) is str:
            self.name = system_name
        else:
            raise TypeError("system_name must be str")
        if type(system_path) is str:
            self.path = system_path
        else:
            raise TypeError("system_path must be str")
        if type(system_short_name) is str:
            self.short_name = system_short_name
        else:
            raise TypeError("system_short_name must be str")
        if type(system_type) is str:
            self.type = system_type
        else:
            raise TypeError("system_type must be str")
        self.company = system_company
        self.description = system_description
        self.media = system_medias
        self.extensions = system_extensions
        if type(system_scraped) is bool:
            self.scraped = system_scraped
        else:
            raise TypeError("system_scraped must be bool")
        if type(system_manual_edit) is bool:
            self.manual_edit = system_manual_edit
        else:
            raise TypeError("system_manual_edit must be bool")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: LocaleClass):
        if type(description) is LocaleClass:
            self._description = description
        elif description is None:
            pass
        else:
            raise TypeError("description must be locale")

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, medias: List[MediaClass]):
        if type(medias) is List[MediaClass]:
            self._media = medias
        elif medias is None:
            pass
        else:
            raise TypeError("medias must be list of media_class")

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, company: company):
        if type(company) is company:
            self._company = company
        elif company is None:
            pass
        else:
            raise TypeError("company must be company")

    @property
    def extensions(self):
        return self._extensions

    @extensions.setter
    def extensions(self, extensions: List[str]):
        if type(extensions) is List[str]:
            temp_ext = []
            for extension in extensions:
                if extension.startswith("."):
                    temp_ext.append(extension)
                else:
                    temp_ext.append(f".{extension}")
            self._extensions = temp_ext
        elif extensions is None:
            pass
        else:
            raise TypeError("extensions must be list of str")

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'path': self.path, 'company': self.company.to_dict(),
                'short_name': self.short_name, 'type': self.type, 'description': self.description.to_dict(),
                'media': [media.to_dict() for media in self.media], 'extensions': self.extensions,
                'scraped': self.scraped, 'manual_edit': self.manual_edit}


class GameClass:
    id: int = None
    name: str = None
    _description: LocaleClass = None
    year: int = None
    _developer: CompanyClass = None
    _publisher: CompanyClass = None
    _media: List[MediaClass] = None
    _genres: List[GenreClass] = None
    _roms: List[RomClass] = None
    _system: SystemClass = None
    family: List[str] = None
    min_players: int = None
    max_players: int = None
    rating: float = None
    scraped: bool = False
    manual_edit: bool = False

    def __init__(self, game_id: int = None, game_name: str = None, game_description: LocaleClass = None,
                 game_year: int = None, game_developer: CompanyClass = None, game_publisher: CompanyClass = None,
                 game_media: List[MediaClass] = None, game_genres: List[GenreClass] = None,
                 game_roms: List[RomClass] = None, game_system: SystemClass = None, game_family: List[str] = None,
                 game_min_players: int = None, game_max_players: int = None, game_rating: float = None,
                 game_scraped: bool = False, game_manual_edit: bool = False):
        if type(game_id) is int:
            self.id = game_id
        else:
            raise TypeError("game_id must be int")

        if type(game_name) is str:
            self.name = game_name
        else:
            raise TypeError("game_name must be str")

        if type(game_year) is int:
            self.year = game_year
        elif game_year is None:
            pass
        else:
            raise TypeError("game_year must be int")

        if type(game_family) is List[str]:
            self.family = game_family
        elif game_family is None:
            pass
        else:
            raise TypeError("game_family must be list of str")

        if type(game_min_players) is int:
            self.min_players = game_min_players
        elif game_min_players is None:
            pass
        else:
            raise TypeError("game_min_players must be int")

        if type(game_max_players) is int:
            self.max_players = game_max_players
        elif game_max_players is None:
            if self.min_players is not None:
                self.max_players = self.min_players
            else:
                pass
        else:
            raise TypeError("game_max_players must be int")

        if type(game_rating) is float:
            self.rating = game_rating
        elif game_rating is None:
            pass
        else:
            raise TypeError("game_rating must be float")

        if type(game_scraped) is bool:
            self.scraped = game_scraped
        else:
            raise TypeError("game_scraped must be bool")

        if type(game_manual_edit) is bool:
            self.manual_edit = game_manual_edit
        else:
            raise TypeError("game_manual_edit must be bool")

        self.description = game_description
        self.developer = game_developer
        self.publisher = game_publisher
        self.media = game_media
        self.genres = game_genres
        self.roms = game_roms
        self.system = game_system

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: LocaleClass):
        if type(description) is LocaleClass:
            self._description = description
        elif description is None:
            pass
        else:
            raise TypeError("description must be locale")

    @property
    def developer(self):
        return self._developer

    @developer.setter
    def developer(self, developer: CompanyClass):
        if type(developer) is CompanyClass:
            self._developer = developer
        elif developer is None:
            pass
        else:
            raise TypeError("developer must be company")

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher: CompanyClass):
        if type(publisher) is CompanyClass:
            self._publisher = publisher
        elif publisher is None:
            pass
        else:
            raise TypeError("publisher must be company")

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, medias: List[MediaClass]):
        if type(medias) is List[MediaClass]:
            self._media = medias
        elif medias is None:
            pass
        else:
            raise TypeError("medias must be list of media_class")

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres: List[GenreClass]):
        if type(genres) is List[GenreClass]:
            self._genres = genres
        elif genres is None:
            pass
        else:
            raise TypeError("genres must be list of genre_class")

    @property
    def roms(self):
        return self._roms

    @roms.setter
    def roms(self, roms: List[RomClass]):
        if type(roms) is List[RomClass]:
            self._roms = roms
        elif roms is None:
            pass
        else:
            raise TypeError("roms must be list of rom_class")

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, system: SystemClass):
        if type(system) is SystemClass:
            self._system = system
        elif system is None:
            pass
        else:
            raise TypeError("system must be system_class")

    def __str__(self):
        return f"{self.name} ({self.year})"

    def __repr__(self):
        return f"{self.name} ({self.year})"

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description.to_dict(),
                'year': self.year, 'developer': self.developer.to_dict(), 'publisher': self.publisher.to_dict(),
                'media': [media.to_dict() for media in self.media], 'genres': [genre.to_dict() for genre in self.genres],
                'roms': [rom.to_dict() for rom in self.roms], 'system': self.system.to_dict(), 'family': self.family,
                'min_players': self.min_players, 'max_players': self.max_players, 'rating': self.rating,
                'scraped': self.scraped, 'manual_edit': self.manual_edit}




#########################################################


