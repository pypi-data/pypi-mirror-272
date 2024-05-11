import os, time, pickle
from typing import Iterable
from datamana.base import Base
import numpy as np

class Server(Base):
    def __init__(self, name, dataloader: Iterable):
        super().__init__(name)
        self.dataloader = dataloader
        self.iterloader = iter(self.dataloader)
        self.oflags = os.O_CREAT | os.O_RDWR
        self.data_id = 0
        self.max_data_id = 2**31 - 1

    def next(self):
        try:
            data = next(self.iterloader)
        except StopIteration:
            self.iterloader = iter(self.dataloader)
            data = next(self.iterloader)
        shm = self.get_shm(self.data_share_name, data.nbytes, oflag=self.oflags)
        self.write_numpy(shm, data)

        meta_data = {
            'shape': data.shape,
            'dtype': data.dtype.name,
            'id': self.data_id,
        }
        meta_data_pkl = pickle.dumps(meta_data)
        pkl_size = len(meta_data_pkl)
        shm = self.get_shm(self.data_meta_name, pkl_size, oflag=self.oflags)
        self.write_byte(shm, meta_data_pkl, pkl_size)
        self.data_id += 1
        if self.data_id >= self.max_data_id:
            self.data_id = 0

    def serve(self):
        self.next()

        while True:
            # wait client signal
            ret = self.event.wait()
            loop = ret
            # clean all signal
            while loop == 0:
                loop = self.event.trywait()

            if ret == 0:
                self.sem.wait()
                self.next()
                self.sem.post()
            else:
                print(os.strerror(ret))
                time.sleep(1)

class Client(Base):
    def __init__(self, name):
        super().__init__(name)
        self.pid = os.getpid()
        self.oflags = os.O_RDWR
        self.data_id = -1

    def next(self):
        while True:
            self.sem.wait()

            shm_meta = self.get_shm(self.data_meta_name, 0, oflag=self.oflags)
            meta_data = pickle.loads(shm_meta.buf)

            if self.data_id != meta_data['id']:
                self.data_id = meta_data['id']
                shape = meta_data['shape']
                dtype = np.dtype(meta_data['dtype'])

                shm_data = self.get_shm(self.data_share_name, 0, oflag=self.oflags)
                data = np.ndarray(shape, dtype=dtype, buffer=shm_data.buf).copy()

                self.sem.post()
                return data
            else:
                self.sem.post()
                self.event.post()
