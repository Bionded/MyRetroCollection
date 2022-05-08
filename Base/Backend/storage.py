from sqlalchemy import Column, Integer, String, Boolean, create_engine, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
import logging
from Base.config_manager import Config_manager
import os

Base = declarative_base()


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


class romDec(Base):
    __tablename__ = 'roms'

    id = Column(Integer, primary_key=True,
                unique=True,
                autoincrement=True)
    name = Column(String)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    platform = relationship('platformDec', backref='roms', lazy='subquery')
    description = Column(String)
    developer = Column(String)
    release = Column(String)
    md5sum = Column(String, unique=True)
    sha1sum = Column(String, unique=True)
    path = Column(String)
    genre = Column(String)
    rating = Column(Float)
    language = Column(String)
    publisher = Column(String)
    players = Column(Integer)
    boxart_path = Column(String)
    screenshot_path = Column(String)
    video_path = Column(String)
    logo_path = Column(String)
    region = Column(String)
    man_edit = Column(Boolean)
    scraped = Column(Boolean)
    exists = Column(Boolean)

    def __init__(self, options: dict = None):
        for key, value in options.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'Rom {self.name}'

    def update(self, options: dict):
        for key, value in options.items():
            setattr(self, key, value)

    def export(self):
        exportdict=dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                exportdict[key]=value
        return exportdict


class SQLStorage():

    #def __init__(self, config: Configger, ):
    def __init__(self, config=Config_manager(), logger=logging.getLogger("__backend__")):
        self.logging = logging.getLogger("__main__")
        self.config = config
        self.logger = logger
        # self.db_type = config.get()
        db_path = "DB/sqlite.db"
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
            self.session.add(romDec(rom))
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
                self.session.add(romDec(rom))
        self.session.commit()
        self.session.close()
