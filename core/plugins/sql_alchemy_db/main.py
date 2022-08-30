from sqlalchemy import Column, Integer, String, Boolean, create_engine, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
import logging
import os

Base = declarative_base()

class RomDec(Base):
    __tablename__ = 'roms'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    rom_size = Column(Integer)
    rom_filename = Column(String)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    game = relationship('gameDec', backref='roms', lazy='subquery')
    rom_crc = Column(String)
    rom_md5 = Column(String)
    rom_sha1 = Column(String)
    beta = Column(Boolean)
    demo = Column(Boolean)
    proto = Column(Boolean)
    hack = Column(Boolean)
    unl = Column(Boolean)
    rom_region = Column(Integer, ForeignKey('platforms.id'))

    def __init__(self, options: dict = None):
        for key, value in options.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Rom {self.name}'

    def update(self, options: dict):
        for key, value in options.items():
            setattr(self, key, value)

    def export(self):
        exportdict = dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                exportdict[key] = value
        return exportdict

class regionDec(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    region_full = Column(String)
    region_short = Column(String)

    def __init__(self, options: dict = None):
        for key, value in options.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Rom {self.name}'

    def update(self, options: dict):
        for key, value in options.items():
            setattr(self, key, value)

    def export(self):
        exportdict = dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                exportdict[key] = value
        return exportdict

class mediaDec(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    media_type = Column(String)
    media_path = Column(String)
    media_region = Column(Integer, ForeignKey('regions.id'))
    media_size = Column(Integer)
    media_format = Column(String)
    media_crc = Column(String)
    media_md5 = Column(String)
    media_sha1 = Column(String)
    media_parent = Column(String)

    def __init__(self, options: dict = None):
        for key, value in options.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Rom {self.name}'

    def update(self, options: dict):
        for key, value in options.items():
            setattr(self, key, value)

    def export(self):
        exportdict = dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                exportdict[key] = value
        return exportdict

class genreDec(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    genre_name = Column(String)

    def __init__(self, options: dict = None):
        for key, value in options.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Rom {self.name}'

    def update(self, options: dict):
        for key, value in options.items():
            setattr(self, key, value)

    def export(self):
        exportdict = dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                exportdict[key] = value
        return exportdict

class platformDec(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    name = Column(String, unique=True, )
    description = Column(String)
    full_name = Column(String)
    folder = Column(String)
    developer = Column(String)
    release = Column(String)
    extensions = Column(String)
    man_edit = Column(Boolean)
    #roms = relationship('romDec', backref='roms', lazy='subquery')

    def __init__(self, options: dict = None):
        for key, value in options.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Platform {self.name}'

    def update(self, options: dict):
        for key, value in options.items():
            setattr(self, key, value)

    def export(self):
        exportdict=dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                exportdict[key]=value
        return exportdict

class gameDec(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    name = Column(String)
    publisher = Column(String)
    developer = Column(String)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    platform = relationship('platformDec', backref='roms', lazy='subquery')
    players = Column(String)
    description = Column(String)
    release = Column(String)
    genre_id = Column(String, ForeignKey('genres.id'))
    genre = relationship('genreDec', lazy='subquery')
    media = relationship('mediaDec',backref= lazy='subquery')
    full_name = Column(String)
    folder = Column(String)
    developer = Column(String)
    extensions = Column(String)



class sql_alchemy_db():

    def __init__(self, plugin_manager):
        self.name = "sql_alchemy_db_plugin"
        self.plugin_type = "database"
        self.version = "0.0.1"
        self.author = "Bionded"
        self.description = "Plugin to provide interface fom db manger"
        self.website = ""
        self.license = "GPLv3"
        self.dependencies = ['sqlalchemy']
        self.plugin_manager = plugin_manager
        self.configs = self.plugin_manager.configs
        self.logger = self.plugin_manager.logger
        db_path = "DB/sqlite.db"

    def enable(self):
        self.engine = create_engine('sqlite:///' + os.path.abspath(db_path))
        self.session = sessionmaker(bind=self.engine, autocommit=True)()
        self.base_class = Base
        self.base_class.metadata.create_all(self.engine)



    def add_platform(self, platform: dict):
        self.session.begin()
        if self.session.query(exists().where(platformDec.name == platform["name"])).scalar():
            q = self.session.query(platformDec).filter(platformDec.name == platform["name"]).one()
            if not q.man_edit:
                q.update(platform)
        else:
            self.session.add(platformDec(platform))
        self.session.commit()
        self.session.close()

    def get_platform(self, platform_name: str):
        if self.session.query(exists().where(platformDec.name == platform_name)).scalar():
            return self.session.query(platformDec).filter(platformDec.name == platform_name).one()

        else:
            return None

    def get_all_platforms(self):
        temp_list = list()
        for platform in self.session.query(platformDec).order_by(platformDec.name):
            temp_list.append(platform.export())
        return temp_list

    def get_all_roms(self):
        temp_list = list()
        for rom in self.session.query(romDec).order_by(romDec.name):
            temp_list.append(rom.export())
        return temp_list

    def add_rom(self, rom: dict, update_exist=True):
        self.session.begin()
        if self.session.query(exists().where(romDec.md5sum == rom["md5sum"] and
                                             romDec.sha1sum == rom["sha1sum"])).scalar() and update_exist:
            q = self.session.query(romDec).filter_by(md5sum=rom["md5sum"], sha1sum=rom["sha1sum"]).one()
            if not q.man_edit:
                q.update(rom)
                #q.man_edit=True
        else:
            self.session.add(platformDec(rom))
        self.session.commit()
        self.session.close()

    def add_rom_list(self, roms: list, update_exist: bool = True):
        self.session.begin()
        for rom in roms:
            if self.session.query(exists().where(romDec.md5sum == rom["md5sum"] and
                                                 romDec.sha1sum == rom["sha1sum"])).scalar() and update_exist:
                q = self.session.query(romDec).filter_by(md5sum=rom["md5sum"], sha1sum=rom["sha1sum"]).one()
                if not q.man_edit:
                    q.update(rom)
                    #q.man_edit=True
            else:
                self.session.add(platformDec(rom))
        self.session.commit()
        self.session.close()



