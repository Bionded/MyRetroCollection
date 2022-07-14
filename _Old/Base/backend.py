from _Old.Base.Backend import filesystem, storage, scanner, importer, collector
from _Old.Base import config_manager
from _Old.Base.logger import load_logger
from queue import Queue
import threading
import time


class Backend:

    def __init__(self):
        conf_path = "config/backend.conf"
        self.configs = config_manager.Config_manager(conf_path).section('Backend')
        self.logger = load_logger(self.configs, "__Backend__")
        self.queue =Queue()


        self.Filesystem = filesystem.getFS(config=self.configs, logger=self.logger)

        self.Storage = storage.SQLStorage(config=self.configs, logger=self.logger)

        self.Importer = importer.Importer(config=self.configs, logger=self.logger,
                                          fs=self.Filesystem)

        self.Scanner = scanner.FileScanner(config=self.configs, filesystem=self.Filesystem,
                                           logger=self.logger)

        self.Collector = collector.Collector(config=self.configs, storage=self.Storage,
                                             importer=self.Importer, filesystem=self.Filesystem,
                                             logger=self.logger)


        self.multithread = self.configs.get_bool("multithread", True)

        self.start_threads()

    def start_threads(self):
        if self.multithread:
            for i in range(1, 8):
                self.threads = threading.Thread(target=self.solo_daemon)
                self.threads.daemon = True
                self.threads.start()

        else:
            self.threads = threading.Thread(target=self.solo_daemon)
            self.threads.daemon = True
            self.threads.start()

    def solo_daemon(self):
        while True:
            if self.queue.empty():
                self.do_work()
            time.sleep(1)
            job = self.queue.get()
            thread = threading.Thread(target=job['func'], args=job['args'])
            thread.start()
            thread.join()
            self.queue.task_done()

    def do_work(self):
        pass
