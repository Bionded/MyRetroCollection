from tinydb import TinyDB, Query
from tinydb.table import Document
import os
from core.utils.types import *


class db_manager:
    def __init__(self, core):
        self.name = "DBManager"
        self.version = "0.0.1"
        self._core = core
        self.config_manager = self._core.config_manager
        self.plugin_manager = self._core.plugin_manager
        self.logs_manager = self._core.logs_manager
        self.logger = self.logs_manager.getLogger(self)
        self.config = self.config_manager.getConfig(self)
        self.db_driver = self.config.getValue('db_driver', 'default')

    def get_db_driver(self):
        if self.db_driver == 'default':
            self.logger.info(self, "Using default db driver")
            return default_db(self)
        driver = self.plugin_manager.doCommand(self, 'get_db_driver', self.db_driver)
        if driver:
            self.logger.info(self, f"Using db driver {self.db_driver}")
            return driver
        else:
            self.logger.error(self, f"db driver {self.db_driver} not found use default")
            return default_db(self)

    def set_db_driver_name(self, driver):
        if self.plugin_manager.getPlugin(driver):
            self.config.setValue('db_driver', driver)
            self.config_manager.saveConfig(self)
            self.logger.info(self, f"db driver set to {driver}")
            return True
        else:
            self.logger.error(self, f"db driver {driver} not found or disabled, driver set to {self.db_driver}")
            return False

    def get_db_driver_name(self):
        return self.db_driver



class default_db:
    def __init__(self, db_manager):
        self.name = "default_db"
        self._db_manager = db_manager
        self.version = self._db_manager.version
        self.config = self._db_manager.config_manager.getConfig(self)
        self.logger = self._db_manager.logs_manager.getLogger(self)
        self.db_filepath = os.path.join(os.getcwd(), self.config.getValue('db_filepath', 'db/db.json'))
        if not os.path.exists(os.path.dirname(self.db_filepath)):
            os.makedirs(os.path.dirname(self.db_filepath))
        self.db = TinyDB(self.db_filepath)
        self.systems_table = self.db.table('systems')
        self.roms_table = self.db.table('roms')
        self.medias_table = self.db.table('media')
        self.locales_table = self.db.table('locales')
        self.genres_table = self.db.table('genres')
        self.companies_table = self.db.table('companies')
        self.games_table = self.db.table('games')
        self.tables = {
            'systems': self.systems_table,
            'roms': self.roms_table,
            'media': self.medias_table,
            'locales': self.locales_table,
            'genres': self.genres_table,
            'companies': self.companies_table,
            'games': self.games_table
        }
        self.query = Query()

    ###########################################
    #Adding items
    ###########################################
    def add_media(self,media: MediaClass, force=False):
        if media.id == None:
            dict_media = media.to_dict()
            del dict_media['id']
            return self.medias_table.insert(dict_media)
        if self.medias_table.contains(doc_id=media.id) and not force:
            media.id = None
            return self.add_media(media, force)
        elif self.medias_table.contains(doc_id=media.id) and force:
            self.medias_table.remove(doc_ids=[media.id])
            dict_media = media.to_dict()
            del dict_media['id']
            ret_id = self.medias_table.insert(Document(dict_media, doc_id=media.id))
            self.logger.debug(self, f"Added media {media}")
            return ret_id
        else:
            dict_media = media.to_dict()
            del dict_media['id']
            ret_id = self.medias_table.insert(Document(dict_media, doc_id=media.id))
            self.logger.debug(self, f"Added media {media}")
            return ret_id

    def add_rom(self, rom: RomClass, force=False):
        if rom.id == None:
            dict_rom = rom.to_dict()
            del dict_rom['id']
            return self.roms_table.insert(dict_rom)
        if self.roms_table.contains(doc_id=rom.id) and not force:
            rom.id = None
            return self.add_rom(rom, force)
        elif self.roms_table.contains(doc_id=rom.id) and force:
            self.roms_table.remove(doc_ids=[rom.id])
            dict_rom = rom.to_dict()
            del dict_rom['id']
            ret_id = self.roms_table.insert(Document(dict_rom, doc_id=rom.id))
            self.logger.debug(self, f"Added rom {rom}")
            return ret_id
        else:
            dict_rom = rom.to_dict()
            del dict_rom['id']
            ret_id = self.roms_table.insert(Document(dict_rom, doc_id=rom.id))
            self.logger.debug(self, f"Added rom {rom}")
            return ret_id
    def add_locale(self, locale: LocaleClass, force=False):
        if locale.id == None:
            dict_locale = locale.to_dict()
            del dict_locale['id']
            return self.locales_table.insert(dict_locale)
        if self.locales_table.contains(doc_id=locale.id) and not force:
            locale.id = None
            return self.add_locale(locale, force)
        elif self.locales_table.contains(doc_id=locale.id) and force:
            self.locales_table.remove(doc_ids=[locale.id])
            dict_locale = locale.to_dict()
            del dict_locale['id']
            ret_id = self.locales_table.insert(Document(dict_locale, doc_id=locale.id))
            self.logger.debug(self, f"Added locale {locale}")
            return ret_id
        else:
            dict_locale = locale.to_dict()
            del dict_locale['id']
            ret_id = self.locales_table.insert(Document(dict_locale, doc_id=locale.id))
            self.logger.debug(self, f"Added locale {locale}")
            return ret_id

    def add_genre(self, genre: GenreClass, force=False):
        if genre.id == None:
            dict_genre = genre.to_dict()
            media_ids = []
            for media in genre.media:
                media_ids.append(self.add_media(media, force=True))
            dict_genre['media'] = media_ids
            del dict_genre['id']
            return self.genres_table.insert(dict_genre)
        if self.genres_table.contains(doc_id=genre.id) and not force:
            genre.id = None
            return self.add_genre(genre, force)
        elif self.genres_table.contains(doc_id=genre.id) and force:
            self.genres_table.remove(doc_ids=[genre.id])
            dict_genre = genre.to_dict()
            del dict_genre['id']
            media_ids = []
            for media in genre.media:
                media_ids.append(self.add_media(media))
            dict_genre['media'] = media_ids
            ret_id = self.genres_table.insert(Document(dict_genre, doc_id=genre.id))
            self.logger.debug(self, f"Added genre {genre}")
            return ret_id
        else:
            dict_genre = genre.to_dict()
            del dict_genre['id']
            media_ids = []
            for media in genre.media:
                media_ids.append(self.add_media(media))
            dict_genre['media'] = media_ids
            ret_id = self.genres_table.insert(Document(dict_genre, doc_id=genre.id))
            self.logger.debug(self, f"Added genre {genre}")
            return ret_id

    def add_company(self, company: CompanyClass, force=False):
        if company.id == None:
            dict_company = company.to_dict()
            del dict_company['id']
            return self.companies_table.insert(dict_company)
        if self.companies_table.contains(doc_id=company.id) and not force:
            company.id = None
            return self.add_company(company, force)
        elif self.companies_table.contains(doc_id=company.id) and force:
            self.companies_table.remove(doc_ids=[company.id])
            media_ids = []
            for media in company.media:
                media_ids.append(self.add_media(media, force=True))
            dict_company = company.to_dict()
            dict_company['media'] = media_ids
            dict_company['description'] = self.add_locale(company.description, force=True)
            del dict_company['id']
            ret_id = self.companies_table.insert(Document(dict_company, doc_id=company.id))
            self.logger.debug(self, f"Added company {company}")
            return ret_id
        else:
            media_ids = []
            for media in company.media:
                media_ids.append(self.add_media(media, force=True))
            dict_company = company.to_dict()
            dict_company['media'] = media_ids
            dict_company['description'] = self.add_locale(company.description, force=True)
            del dict_company['id']
            ret_id = self.companies_table.insert(Document(dict_company, doc_id=company.id))
            self.logger.debug(self, f"Added company {company}")
            return ret_id

    def add_system(self, system: SystemClass, force=False):
        if system.id == None:
            dict_system = system.to_dict()
            del dict_system['id']
            return self.systems_table.insert(dict_system)
        if self.systems_table.contains(doc_id=system.id) and not force:
            system.id = None
            return self.add_system(system, force)
        elif self.systems_table.contains(doc_id=system.id) and force:
            self.systems_table.remove(doc_ids=[system.id])
            dict_system = system.to_dict()
            media_ids = []
            for media in system.media:
                media_ids.append(self.add_media(media, force=True))
            dict_system['media'] = media_ids
            dict_system['description'] = self.add_locale(system.description, force=True)
            dict_system['company'] = self.add_company(system.company, force=True)
            del dict_system['id']
            ret_id = self.systems_table.insert(Document(dict_system, doc_id=system.id))
            self.logger.debug(self, f"Added system {system}")
            return ret_id
        else:
            dict_system = system.to_dict()
            media_ids = []
            for media in system.media:
                media_ids.append(self.add_media(media, force=True))
            dict_system['media'] = media_ids
            dict_system['description'] = self.add_locale(system.description, force=True)
            dict_system['company'] = self.add_company(system.company, force=True)
            del dict_system['id']
            ret_id = self.systems_table.insert(Document(dict_system, doc_id=system.id))
            self.logger.debug(self, f"Added system {system}")
            return ret_id

    def add_game(self, game: GameClass, force=False):
        if game.id == None:
            dict_game = game.to_dict()
            del dict_game['id']
            return self.games_table.insert(dict_game)
        if self.games_table.contains(doc_id=game.id) and not force:
            game.id = None
            return self.add_game(game, force)
        elif self.games_table.contains(doc_id=game.id) and force:
            self.games_table.remove(doc_ids=[game.id])
            dict_game = game.to_dict()
            media_ids = []
            for media in game.media:
                media_ids.append(self.add_media(media))
            dict_game['media'] = media_ids
            dict_game['description'] = self.add_locale(game.description)
            dict_game['genres'] = []
            for genre in game.genres:
                dict_game['genres'].append(self.add_genre(genre))
            dict_game['developer'] = self.add_company(game.developer)
            dict_game['publisher'] = self.add_company(game.publisher)
            dict_game['system'] = self.add_system(game.system)
            dict_game['roms'] = []
            for rom in game.roms:
                dict_game['roms'].append(self.add_rom(rom))
            ret_id = self.games_table.insert(Document(dict_game, doc_id=game.id))
            self.logger.debug(self, f"Added game {game}")
            return ret_id
        else:
            dict_game = game.to_dict()
            media_ids = []
            for media in game.media:
                media_ids.append(self.add_media(media))
            dict_game['media'] = media_ids
            dict_game['description'] = self.add_locale(game.description)
            dict_game['genres'] = []
            for genre in game.genres:
                dict_game['genres'].append(self.add_genre(genre))
            dict_game['developer'] = self.add_company(game.developer)
            dict_game['publisher'] = self.add_company(game.publisher)
            dict_game['system'] = self.add_system(game.system)
            dict_game['roms'] = []
            for rom in game.roms:
                dict_game['roms'].append(self.add_rom(rom))
            ret_id = self.games_table.insert(Document(dict_game, doc_id=game.id))
            self.logger.debug(self, f"Added game {game}")
            return ret_id

    ###########################################
    # Getters
    ###########################################

    def get_media(self, media_id):
        if type(media_id) == str:
            media_id = int(media_id)
        elif type(media_id) != int:
            raise TypeError(f"media_id must be int or str, not {type(media_id)}")

        media = self.medias_table.get(doc_id=media_id)
        if media == None:
            return None
        return MediaClass(media_id=media_id, media_path=media['path'], media_name=media['name'],
                          media_size=media['size'], media_extension=media['extension'], media_md5=media['md5'],
                          media_sha1=media['sha1'], media_crc=media['crc'], media_file_driver=media['file_driver'],
                          media_format=media['format'], media_type=media['type'], is_existing=media['existing'])

    def get_rom(self, rom_id):
        if type(rom_id) == str:
            rom_id = int(rom_id)
        elif type(rom_id) != int:
            raise TypeError(f"rom_id must be int or str, not {type(rom_id)}")

        rom = self.roms_table.get(doc_id=rom_id)
        if rom == None:
            return None
        return RomClass(rom_id=rom_id,rom_path=rom['path'], rom_name=rom['name'], rom_size=rom['size'],
                        rom_extension=rom['extension'], rom_md5=rom['md5'], rom_sha1=rom['sha1'], rom_crc=rom['crc'],
                        rom_file_driver=rom['file_driver'], is_beta=rom['beta'], is_demo=rom['demo'],is_proto=rom['proto'],
                        is_trad=rom['trad'], is_hack=rom['hack'], is_unl=rom['unl'],  is_alt=rom['alt'],
                        is_best=rom['best'], is_netplay=rom['netplay'], is_existing=rom['existing'])

    def get_locale(self, locale_id):
        if type(locale_id) == str:
            locale_id = int(locale_id)
        elif type(locale_id) != int:
            raise TypeError(f"locale_id must be int or str, not {type(locale_id)}")

        locale = self.locales_table.get(doc_id=locale_id)
        if locale == None:
            return None
        return LocaleClass(locale_id=locale_id, locale_strings=locale['strings'],
                           locale_default_language=locale['default_language'])

    def get_genre(self, genre_id):
        if type(genre_id) == str:
            genre_id = int(genre_id)
        elif type(genre_id) != int:
            raise TypeError(f"genre_id must be int or str, not {type(genre_id)}")

        genre = self.genres_table.get(doc_id=genre_id)
        if genre == None:
            return None
        medias = []
        for media in genre['media']:
            medias.append(self.get_media(media))

        return GenreClass(genre_id=genre_id, genre_name=genre['name'], genre_medias=medias)

    def get_company(self, company_id):
        if type(company_id) == str:
            company_id = int(company_id)
        elif type(company_id) != int:
            raise TypeError(f"company_id must be int or str, not {type(company_id)}")

        company = self.companies_table.get(doc_id=company_id)
        if company is None:
            return None
        medias = []
        for media in company['media']:
            medias.append(self.get_media(media))

        company['description'] = self.get_locale(company['description'])

        return CompanyClass(company_id=company_id, company_name=company['name'],
                            company_description=company['description'], company_medias=medias)

    def get_system(self, system_id):
        if type(system_id) == str:
            system_id = int(system_id)
        elif type(system_id) != int:
            raise TypeError(f"system_id must be int or str, not {type(system_id)}")

        system = self.systems_table.get(doc_id=system_id)
        if system == None:
            return None
        medias = []
        for media in system['media']:
            medias.append(self.get_media(media))

            system['description'] = self.get_locale(system['description'])
            system['company'] = self.get_company(system['company'])

        return SystemClass(system_id=system_id, system_name=system['name'],system_path=system['path'],
                           system_company=system['company'], system_short_name=system['short_name'],
                           system_type=system['type'], system_description=system['description'], system_medias=medias,
                           system_extensions=system['extensions'], system_scraped=system['scraped'],
                           system_manual_edit=system['manual_edit'])

    def get_game(self, game_id):
        if type(game_id) == str:
            game_id = int(game_id)
        elif type(game_id) != int:
            raise TypeError(f"game_id must be int or str, not {type(game_id)}")

        game = self.games_table.get(doc_id=game_id)
        if game == None:
            return None

        medias = []
        for media in game['media']:
            medias.append(self.get_media(media))
        genres = []
        for genre in game['genres']:
            genres.append(self.get_genre(genre))
        roms = []
        for rom in game['roms']:
            roms.append(self.get_rom(rom))
        game['description'] = self.get_locale(game['description'])
        game['system'] = self.get_system(game['system'])
        game['developer'] = self.get_company(game['developer'])
        game['publisher'] = self.get_company(game['publisher'])


        return GameClass(game_id=game_id, game_name=game['name'], game_description=game['description'],
                         game_year=game['year'], game_developer=game['developer'], game_publisher=game['publisher'],
                         game_media=medias, game_genres=genres, game_roms=roms, game_system=game['system'],
                         game_family=game['family'], game_min_players=game['min_players'],
                         game_max_players=game['max_players'], game_rating=game['rating'], game_scraped=game['scraped'],
                         game_manual_edit=game['manual_edit'])

    ##########################################
    # Removers
    ##########################################

    def remove_media(self, media_id):
        if type(media_id) == str:
            media_id = int(media_id)
        elif type(media_id) != int:
            raise TypeError(f"media_id must be int or str, not {type(media_id)}")

        self.medias_table.remove(doc_ids=[media_id])

    def remove_rom(self, rom_id):
        if type(rom_id) == str:
            rom_id = int(rom_id)
        elif type(rom_id) != int:
            raise TypeError(f"rom_id must be int or str, not {type(rom_id)}")

        self.roms_table.remove(doc_ids=[rom_id])

    def remove_locale(self, locale_id):
        if type(locale_id) == str:
            locale_id = int(locale_id)
        elif type(locale_id) != int:
            raise TypeError(f"locale_id must be int or str, not {type(locale_id)}")

        self.locales_table.remove(doc_ids=[locale_id])

    def remove_genre(self, genre_id, remove_childs=True):
        if type(genre_id) == str:
            genre_id = int(genre_id)
        elif type(genre_id) != int:
            raise TypeError(f"genre_id must be int or str, not {type(genre_id)}")
        if remove_childs:
            genre = self.genres_table.get(self.query.id == genre_id)

            self.medias_table.remove(doc_ids=genre['media'])

        self.genres_table.remove(doc_ids=[genre_id])

    def remove_company(self, company_id, remove_childs=True):
        if type(company_id) == str:
            company_id = int(company_id)
        elif type(company_id) != int:
            raise TypeError(f"company_id must be int or str, not {type(company_id)}")
        if remove_childs:
            company = self.companies_table.get(self.query.id == company_id)
            self.medias_table.remove(doc_ids=company['media'])
            self.remove_locale(company['description'])

        self.companies_table.remove(doc_ids=[company_id])

    def remove_system(self, system_id, remove_childs=True):
        if type(system_id) == str:
            system_id = int(system_id)
        elif type(system_id) != int:
            raise TypeError(f"system_id must be int or str, not {type(system_id)}")
        if remove_childs:
            system = self.systems_table.get(self.query.id == system_id)

            self.medias_table.remove(doc_ids=system['media'])
            self.remove_locale(system['description'])
            self.remove_locale(system['company'])

        self.systems_table.remove(doc_ids=[system_id])

    def remove_game(self, game_id, remove_childs=True):
        if type(game_id) == str:
            game_id = int(game_id)
        elif type(game_id) != int:
            raise TypeError(f"game_id must be int or str, not {type(game_id)}")
        if remove_childs:
            game = self.games_table.get(self.query.id == game_id)
            self.medias_table.remove(doc_ids=game['media'])
            self.genres_table.remove(doc_ids=game['genres'])
            self.roms_table.remove(doc_ids=game['roms'])
            self.remove_locale(game['description'])
            self.remove_system(game['system'])
            self.remove_locale(game['developer'])
            self.remove_locale(game['publisher'])

        self.games_table.remove(self.query.id == game_id)

    ##########################################
    # Updaters
    ##########################################

    def update_media(self, media: MediaClass):
        if type(media) != MediaClass:
            raise TypeError(f"media must be MediaClass, not {type(media)}")

        if self.medias_table.contains(self.query.id == media.id):
            self.medias_table.update(media.to_dict(), self.query.id == media.id)
            return media.id
        else:
            return self.add_media(media)

    def update_rom(self, rom: RomClass):
        if type(rom) != RomClass:
            raise TypeError(f"rom must be RomClass, not {type(rom)}")

        if self.roms_table.contains(self.query.id == rom.id):
            self.roms_table.update(rom.to_dict(), self.query.id == rom.id)
            return rom.id
        else:
            return self.add_rom(rom)

    def update_locale(self, locale: LocaleClass):
        if type(locale) != LocaleClass:
            raise TypeError(f"locale must be LocaleClass, not {type(locale)}")

        if self.locales_table.contains(self.query.id == locale.id):
            self.locales_table.update(locale.to_dict(), self.query.id == locale.id)
            return locale.id
        else:
            return self.add_locale(locale)

    def update_genre(self, genre: GenreClass):
        if type(genre) != GenreClass:
            raise TypeError(f"genre must be GenreClass, not {type(genre)}")


        if self.genres_table.contains(self.query.id == genre.id):
            medias = []
            for media in genre.media:
                medias.append(self.update_media(media))
            genre_dict = genre.to_dict()
            genre_dict['media'] = medias
            self.genres_table.update(genre_dict, self.query.id == genre.id)
            return genre.id
        else:
            return self.add_genre(genre)

    def update_company(self, company: CompanyClass):
        if type(company) != CompanyClass:
            raise TypeError(f"company must be CompanyClass, not {type(company)}")

        if self.companies_table.contains(self.query.id == company.id):
            medias = []
            for media in company.media:
                medias.append(self.update_media(media))
            company_dict = company.to_dict()
            company_dict['media'] = medias
            company_dict['description'] = self.update_locale(company.description)
            self.companies_table.update(company_dict, self.query.id == company.id)
            return company.id
        else:
            return self.add_company(company)

    def update_system(self, system: SystemClass):
        if type(system) != SystemClass:
            raise TypeError(f"system must be SystemClass, not {type(system)}")

        if self.systems_table.contains(self.query.id == system.id):
            medias = []
            for media in system.media:
                medias.append(self.update_media(media))
            system_dict = system.to_dict()
            system_dict['media'] = medias
            system_dict['description'] = self.update_locale(system.description)
            system_dict['company'] = self.update_locale(system.company)
            self.systems_table.update(system_dict, self.query.id == system.id)
            return system.id
        else:
            return self.add_system(system)

    def update_game(self, game: GameClass):
        if type(game) != GameClass:
            raise TypeError(f"game must be GameClass, not {type(game)}")

        if self.games_table.contains(self.query.id == game.id):
            medias = []
            for media in game.media:
                medias.append(self.update_media(media))
            genres = []
            for genre in game.genres:
                genres.append(self.update_genre(genre))
            roms = []
            for rom in game.roms:
                roms.append(self.update_rom(rom))
            game_dict = game.to_dict()
            game_dict['media'] = medias
            game_dict['genres'] = genres
            game_dict['roms'] = roms
            game_dict['system'] = self.update_system(game.system)
            game_dict['description'] = self.update_locale(game.description)
            game_dict['developer'] = self.update_locale(game.developer)
            game_dict['publisher'] = self.update_locale(game.publisher)
            self.games_table.update(game_dict, self.query.id == game.id)
            return game.id
        else:
            return self.add_game(game)

    ##########################################
    # Non-Specified tables functions
    ##########################################

    def get_all_tables(self):
        return self.db.tables

    def create_table(self, table_name: str):
        keys = 'here for future use and to avoid errors when create tables in another driver'
        if type(table_name) != str:
            raise TypeError(f"table_name must be str, not {type(table_name)}")
        if table_name in self.db.tables:
            self.logger.info(f"Table {table_name} already exists")
        else:
            self.tables[table_name] = self.db.table(table_name)
            self.logger.info(f"Table {table_name} created")

    def find_in_table(self,table: str, query_value, query_property: str = 'id'):
        if table not in self.db.tables:
            raise ValueError(f"Table {table} not found")
        if query_property not in self.db.tables[table].columns:
            raise ValueError(f"Property {query_property} not found in table {table}")
        if query_property == 'id':
            return self.db.tables[table].get(doc_id=query_value)
        else:
            return self.tables[table].search(self.query[query_property] == query_value)

    def add_to_table(self, table: str, item: dict):
        if table not in self.db.tables:
            raise ValueError(f"Table {table} not found")
        if type(item) != dict:
            raise TypeError(f"item must be dict, not {type(item)}")
        if 'id' in item.keys():
            docid = item['id']
            del item['id']
            self.db.tables[table].insert(Document(item, doc_id=docid))
        else:
            return self.tables[table].insert(item)

    def update_in_table(self, table: str, item: dict, query_property: str = 'id'):
        if table not in self.db.tables:
            raise ValueError(f"Table {table} not found")
        if type(item) != dict:
            raise TypeError(f"item must be dict, not {type(item)}")
        if query_property not in item.keys():
            raise ValueError(f"Property {query_property} not found in item")
        self.tables[table].update(item, self.query[query_property] == item[query_property])

    def delete_from_table(self, table: str, query_value, query_property: str = 'id'):
        if table not in self.db.tables:
            raise ValueError(f"Table {table} not found")
        if query_property not in self.db.tables[table].columns:
            raise ValueError(f"Property {query_property} not found in table {table}")
        self.tables[table].remove(self.query[query_property] == query_value)

    def delete_all_from_table(self, table: str):
        if type(table) != str:
            raise TypeError(f"table must be str, not {type(table)}")
        if table not in self.db.tables:
            raise ValueError(f"Table {table} not found")
        self.tables[table].truncate()

    def get_all_from_table(self, table: str):
        if type(table) != str:
            raise TypeError(f"table must be str, not {type(table)}")
        if table not in self.db.tables:
            raise ValueError(f"Table {table} not found")
        return self.tables[table].all()

    ##########################################
    # Utilities
    ##########################################

