import os, time, pickle
from multiprocessing import shared_memory
from typing import Iterable
from datamana.base import Base
import numpy as np

class Server(Base):
    def __init__(self, name, dataloader: Iterable):
        super().__init__(name)
        self.dataloader = dataloader
        self.iterloader = iter(self.dataloader)

    def next(self):
        try:
            data = next(self.iterloader)
        except StopIteration:
            self.iterloader = iter(self.dataloader)
            data = next(self.iterloader)
        self.write_shared_data(self.data_share_name, data, data.nbytes)

        meta_data = {
            'shape': data.shape,
            'dtype': data.dtype.name,
            'pids': set(),
        }
        meta_data_pkl = pickle.dumps(meta_data)
        self.write_shared_data(self.data_meta_name, meta_data_pkl, len(meta_data_pkl))

    def serve(self):
        self.next()

        while True:
            ret, msg, msg_prio = self.server_recv()
            if ret == 0:
                self.sem.wait()
                self.next()
                self.server_send("")
                self.sem.post()
            else:
                print(os.strerror(ret))
                time.sleep(1)

class Client(Base):
    def __init__(self, name):
        super().__init__(name)
        self.pid = os.getpid()

    def next(self):
        while True:
            self.sem.wait()

            shm_meta_data = shared_memory.SharedMemory(self.data_meta_name)
            meta_data = pickle.loads(shm_meta_data.buf)
            shm_meta_data.close()

            if self.pid not in meta_data['pids']:
                shape = meta_data['shape']
                dtype = np.dtype(meta_data['dtype'])

                shm_data = shared_memory.SharedMemory(self.data_share_name)
                data = np.ndarray(shape, dtype=dtype, buffer=shm_data.buf).copy()
                shm_data.close()

                meta_data['pids'].add(self.pid)
                meta_data_pkl = pickle.dumps(meta_data)
                self.write_shared_data(self.data_meta_name, meta_data_pkl, len(meta_data_pkl))
                self.sem.post()
                return data
            else:
                self.client_send("")
                self.sem.post()
                self.client_recv()
