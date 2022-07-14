"""This Code taken from PysonDB
https://github.com/pysonDB/pysonDB
Authors = Adwaith Rajesh andFredy Somy
Thank you and sorry. I change some code for my comfort :)
"""

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Union, Pattern
from filelock import FileLock
from _Old.Base.Backend.Classes.platform import Platform,Rom


class IdNotFoundError(Exception):
    """Exception raised if id not found.

    Attributes:
        pk -- primary key / id
    """

    def __init__(self, pk: str) -> None:
        self.pk = pk

    def __str__(self) -> str:
        return f"Id {self.pk!r} does not exist in the JSON db"

class IdAlreadyExistsError(Exception):
    """Exception raised if id not found.

    Attributes:
        pk -- primary key / id
    """

    def __init__(self, pk: str) -> None:
        self.pk = pk

    def __str__(self) -> str:
        return f"Id {self.pk!r} already exist in the JSON db"


class DataNotFoundError(Exception):
    """Exception raised if id not found.

    Attributes:
        data
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def __str__(self) -> str:
        return f"The data {self.data!r} does not exists in JSON db"


class SchemaError(Exception):
    """Exception raised for field/key errors."""

    def __init__(self, *args) -> None:
        self.args = args

    def __str__(self) -> str:
        return str(self.args)


# constants
EMPTY_DATA: Dict[str, Any] = { "platform": Platform().__dict__, "roms": []}

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("__main__")
logger.setLevel(logging.DEBUG)


# util functions
def create_db(filename: str, create_file: bool = True) -> True:
    def create(filename: str, data: str) -> None:
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "w") as db_file:
            db_file.write(data)

    if filename.endswith(".json"):
        if create_file and not os.path.exists(filename):
            create(filename, json.dumps(EMPTY_DATA))


# the JSON DB


class JsonDatabase:
    def __init__(self, filename: str, log: bool = False, delete_not_exist: bool = False) -> None:
        create_db(filename)  # create the JSON file if it doesn't exists
        sdx = Path(filename)

        self.del_not_exist = delete_not_exist
        self.filename = filename
        self.lock = FileLock("{}.lock".format(self.filename))
        self.base_folder = os.path.dirname(self.filename)
        self.hashsums = self._getHashes()

        if not log:
            self._stop_log()

        logger.info("Database Filename: {0}".format(sdx))


    def _cast_id(self, pk) -> str:
        return pk

    def _get_load_function(self) -> Callable[..., Any]:
        return json.load

    def _get_dump_function(self) -> Callable[..., Any]:
        return json.dump


    @staticmethod
    def _stop_log() -> None:
        logging.getLogger("pysondb").disabled = True
        logging.getLogger("filelock").disabled = True

    def set_platform(self, new_platform: Platform) -> Dict[str, Any]:
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                try:
                    logger.debug("Set platform params; {0}".format(new_platform))
                    db_data["platform"] = new_platform.__dict__
                    db_file.seek(0)
                    self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)
                    return new_platform.__dict__
                except IndexError:
                    db_data["platform"] = new_platform
                    logger.debug("Add first data entry; {0}".format(new_platform))
                    db_file.seek(0)
                    self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)
                return new_platform.__dict__

    def get_platform(self) -> Platform:
        temp_platform = Platform()
        with self.lock:
            try:
                with open(self.filename, "r", encoding="utf8") as db_file:
                    db_data = self._get_load_function()(db_file)
                data = db_data["platform"]
                temp_platform.fromDict(data)
                return temp_platform
            except:
                return temp_platform

    def add(self, new_data: Rom) -> str:
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                try:
                    if set(db_data["roms"][0].keys()) == set(new_data.keys()):

                        logger.debug("Append new rom; {0}".format(new_data))
                        if new_data.hashsum is None:
                            new_data.setup(self.base_folder)
                        if new_data.hashsum in self.hashsums:
                            raise IdAlreadyExistsError(new_data.hashsum)
                        else:
                            db_data["roms"].append(new_data.__dict__)
                            self.hashsums.append(new_data.hashsum)
                            db_file.seek(0)
                            self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)
                            return new_data.hashsum
                    else:
                        raise SchemaError(
                            "db_keys: "
                            + ",".join(sorted(list(db_data["roms"][0].keys()))),
                            "new_data_keys: "
                            + ",".join(
                                sorted(list(new_data.keys()))
                            ),
                        )
                except IndexError:
                    new_data.get_hash(self.base_folder)
                    db_data["roms"].append(new_data.__dict__)
                    logger.debug("Add first data entry; {0}".format(new_data.__dict__))
                    db_file.seek(0)
                    self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)
                return new_data.hashsum

    def addMany(self, new_data: List[Rom]) -> None:
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                if db_data['roms']:
                    db_keys, index_keys = db_data["roms"], [self.id_fieldname]
                else:
                    db_keys, index_keys = new_data, None

                keys = set(db_keys[0].keys())

                for d in new_data:
                    d_keys = set(d.keys() | index_keys) if index_keys else set(d.keys())
                    if keys == d_keys:
                        if d.hashsum is None:
                            d.setup(self.base_folder)

                        if d.hashsum not in self.hashsums:
                            db_data["roms"].append(d.__dict__)
                            self.hashsums.append(d.hashsum)
                            db_file.seek(0)
                    else:
                        raise SchemaError(
                            "db_keys: "
                            + ",".join(sorted(list(db_data["roms"][0].keys()))),
                            "new_data_keys: "
                            + ",".join(
                                sorted(list(d.keys()))
                            ),
                        )
                self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)

    def getAllRoms(self) -> List[Rom]:
        db_data = self._getAll()

        temp_list = []
        for drom in db_data:
            temp_rom = Rom().fromDict(drom)
            temp_list.append(temp_rom)

        return temp_list

    def _getAll(self) -> List[Dict[str, Any]]:
        with self.lock:
            with open(self.filename, "r", encoding="utf8") as db_file:
                db_data = self._get_load_function()(db_file)

            return db_data["roms"]

    def _getHashes(self) -> List[str]:
        with self.lock:
            with open(self.filename, "r", encoding="utf8") as db_file:
                db_data = self._get_load_function()(db_file)
                hash_list = list()
                for rom in db_data['roms']:
                    hash_list.append(rom['_hashsum'])

            return hash_list

    def get(self, num: int = 1) -> List[Rom]:
        temp_list = []
        with self.lock:
            try:
                with open(self.filename, "r", encoding="utf8") as db_file:
                    db_data = self._get_load_function()(db_file)
                if num <= len(db_data["roms"]):
                    data = db_data["roms"][0: int(num)]
                    for drom in data:
                        temp_rom = Rom().fromDict(drom)
                        temp_list.append(temp_rom)
                    return temp_list
                else:
                    logger.info(
                        "The length you have given {} \n Length of the database items= {}".format(
                            num, len(db_data["roms"])
                        )
                    )
                    return temp_list
            except:
                return temp_list

    def getTopOfParam(self, param: str = 'name', num: int = 1, reverse_sort: bool = False) -> List[Rom]:
        temp_list = []
        with self.lock:
            try:
                with open(self.filename, "r", encoding="utf8") as db_file:
                    db_data = self._get_load_function()(db_file)
                if param in db_data["roms"][0].keys():
                    sorted_data = sorted(db_data["roms"], key=lambda d: d[param], reverse=not reverse_sort)
                else:
                    raise SchemaError(
                        "db_keys: "
                        + ",".join(sorted(list(db_data["roms"][0].keys()))),
                        "needed param: "
                        + param,
                    )
                if num <= len(db_data["roms"]):
                    data = sorted_data[0: int(num)]
                    for drom in data:
                        temp_list.append(Rom().fromDict(drom))
                    return temp_list
                else:
                    for drom in sorted_data:
                        temp_list.append(Rom().fromDict(drom))
                    return temp_list
            except:
                return temp_list

    def getByhash(self, pk: str) -> Rom:
        if len(pk) == 32:
            selfid = '_md5sum'
        elif len(pk) == 40:
            selfid = '_sha1sum'
        else:
            selfid = '_hashsum'
        with self.lock:
            temp_rom = Rom()
            try:
                with open(self.filename, "r", encoding="utf8") as db_file:
                    db_data = self._get_load_function()(db_file)
                for d in db_data["roms"]:
                    if d[selfid] == self._cast_id(pk):
                        temp_rom.fromDict(d)
                        return temp_rom
                raise IdNotFoundError(pk)
            except:
                raise IdNotFoundError(pk)

    def getByName(self, name: str) -> List[Rom]:
        with self.lock:
            temp_list = []
            try:
                with open(self.filename, "r", encoding="utf8") as db_file:
                    db_data = self._get_load_function()(db_file)
                for d in db_data["roms"]:
                    if name in d['name']:
                        temp_rom = Rom().fromDict(d)
                        temp_list.append(temp_rom)
                return temp_list
            except:
                return temp_list

    def getByQuery(self, query: Dict[str, Any]) -> List[Rom]:
        with self.lock:
            result = []
            with open(self.filename, "r") as db_file:
                db_data = self._get_load_function()(db_file)
                for d in db_data["roms"]:
                    if all(x in d and d[x] == query[x] for x in query):
                        result.append(d)
            return (
                result

            )

    def reSearch(self, key: str, _re: Union[str, Pattern[str]]) -> List[Rom]:

        pattern = _re
        if not isinstance(_re, re.Pattern):
            pattern = re.compile(str(_re))

        items = []
        data = self._getAll()

        for d in data:
            for k in d.keys():
                if re.match(pattern, str(d[k])) and k == key:
                    items.append(Rom().fromDict(d))
                    continue

        return items

    def updateByListRoms(self, roms: List[Rom],) -> None:
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                result = []
                hashes_list = list()
                for new_rom in roms:
                    hashes_list.append(new_rom.hashsum)
                for d in db_data["roms"]:
                    if d['hashsum'] in hashes_list:
                        for new_rom in roms:
                            if d['hashsum'] == new_rom.hashsum:
                                d.update(new_rom.__dict__)

                    result.append(d)

                db_data["roms"] = result
                db_file.seek(0)
                db_file.truncate()
                self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)

    def updateByHash(self, pk: str, new_data: Rom) -> None:
        updated = False
        if len(pk) == 32:
            selfid = '_md5sum'
        elif len(pk) == 40:
            selfid = '_sha1sum'
        else:
            selfid = '_hashsum'

        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                result = []
                if set(new_data.keys()).issubset(db_data["roms"][0].keys()):
                    for d in db_data["roms"]:
                        if d[selfid] == pk:
                            Platform().fromDict(d).fromDict(new_data.__dict__)
                            updated = True

                        result.append(d)

                    if not updated:
                        raise IdNotFoundError(pk)
                    db_data["roms"] = result
                    db_file.seek(0)
                    db_file.truncate()
                    self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)
                else:
                    raise SchemaError(
                        "db_keys: " + ",".join(sorted(db_data.keys())),
                        "new_keys: " + ",".join(sorted(new_data.keys())),
                    )

    def deleteByHash(self, pk: str, delete_files: bool = False) -> bool:
        if len(pk) == 32:
            selfid = '_md5sum'
        elif len(pk) == 40:
            selfid = '_sha1sum'
        else:
            selfid = '_hashsum'
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                result = []
                found = False

                for d in db_data["roms"]:
                    if d[selfid] == pk:
                        found = True
                        if delete_files:
                            Rom().fromDict(d).delete_files(self.base_folder)
                    else:
                        result.append(d)

                if not found:
                    raise IdNotFoundError(pk)

                db_data["roms"] = result
                db_file.seek(0)
                db_file.truncate()
                self._get_dump_function()(db_data, db_file, ensure_ascii=False)
            return True

    def deleteRoms(self, roms: List[Rom], delete_files: bool = False):
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                for rom in roms:
                    if delete_files:
                        rom.delete_files(self.base_folder)
                    db_data["roms"].remove(rom.__dict__)
                db_file.seek(0)
                db_file.truncate()
                self._get_dump_function()(db_data, db_file, ensure_ascii=False)
            return True

    def clearDB(self) -> None:
        with self.lock:
            with open(self.filename, "w") as f:
                f.write(json.dumps(EMPTY_DATA))

    def clearRoms(self) -> None:
        with self.lock:
            with open(self.filename, "r+") as db_file:
                db_data = self._get_load_function()(db_file)
                db_data["roms"] = []
                db_file.seek(0)
                db_file.truncate()
                self._get_dump_function()(db_data, db_file, ensure_ascii=False)


    # def updateByQuery(self, db_dataset: Dict[str, Any], new_dataset: Dict[str, Any]) -> None:
    #     with self.lock:
    #         with open(self.filename, "r+") as db_file:
    #             db_data = self._get_load_function()(db_file)
    #             result = []
    #             found = False
    #             if set(db_dataset.keys()).issubset(db_data["roms"][0].keys()) and set(
    #                     new_dataset.keys()
    #             ).issubset(db_data["roms"][0].keys()):
    #                 for d in db_data["roms"]:
    #                     if all(x in d and d[x] == db_dataset[x] for x in db_dataset):
    #                         if set(new_dataset.keys()).issubset(
    #                                 db_data["roms"][0].keys()
    #                         ):
    #                             d.update(new_dataset)
    #                             result.append(d)
    #                             found = True
    #                     else:
    #                         result.append(d)
    #
    #                 if not found:
    #                     raise DataNotFoundError(db_dataset)
    #
    #                 db_data["roms"] = result
    #                 db_file.seek(0)
    #                 db_file.truncate()
    #                 self._get_dump_function()(db_data, db_file, indent=3, ensure_ascii=False)
    #             else:
    #                 raise SchemaError(
    #                     "db_dataset_keys: " + ",".join(sorted(list(db_dataset.keys()))),
    #                     "db_keys: " + ",".join(sorted(list(db_data["roms"][0].keys()))),
    #                     "new_dataset_keys: "
    #                     + ",".join(sorted(list(new_dataset.keys()))),
    #                 )

    def close(self):
        self.lock.release()
        try:
            os.remove(self.lock.lock_file)
            # Probably another instance of the application
            # that acquired the file lock.
        except OSError:
            pass
        return None

getDB = JsonDatabase
