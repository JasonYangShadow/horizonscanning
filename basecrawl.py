from exception import Type,TeleException
from abc import ABC, abstractmethod
from config import Config
import multiprocessing
import queue

class BaseCrawl:
    def __init__(self, name, description, config_path = 'config.ini', queue_size = 10000):
        self.name = name
        self.desc = description
        self.config = Config(config_path)
        self.queue = queue.Queue(queue_size)

    @abstractmethod
    def request(self, param = None):
        None

    def save2queue(self,req):
        for r in req:
            if self.queue.full():
                raise TeleException(Type.FullException,'queue is full')
            else:
                self.queue.put(r)

    def run(self, param, syn = True):
        if syn:
            data = self.request(param)
            if data is not None:
                self.resolve(data)
        else:
            while True:
                self.request(param)
                if not self.queue.empty():
                    data = self.queue.get()
                    p = multiprocessing.Process(target = self.resolve, args = (data,))
                    p.start()
                    p.join()

    @abstractmethod
    def resolve(self, data = None):
        None
