import os, mmap
from datamana._C import (
    Semaphore as __Semaphore,
    MQueue as __MQueue,
    SharedMemory as __SharedMemory,
)

class Semaphore(__Semaphore):
    def __init__(self, name, oflag=os.O_CREAT | os.O_RDWR, mode=0o600, value=1):
        super().__init__()
        errno = self.open(name, oflag, mode, value)
        if errno != 0:
            raise RuntimeError(f'create Semaphore failed! <{os.strerror(errno)}>')

del __Semaphore

class MQueue(__MQueue):
    def __init__(self, name, oflag=os.O_CREAT | os.O_RDWR, mode=0o600, msgsize=1, maxmsg=1):
        super().__init__()
        self.msgsize = msgsize
        self.maxmsg = maxmsg
        name = '/' + name
        errno = self.open(name, oflag, mode)
        if errno != 0:
            raise RuntimeError(f'create MQueue failed! <{os.strerror(errno)}>')

del __MQueue

class SharedMemory(__SharedMemory):
    def __init__(self, name, size, oflag=os.O_CREAT | os.O_RDWR, mode=0o600):
        if size < 0:
            raise ValueError("'size' must be a positive integer")
        super().__init__()
        name = '/' + name
        errno = self.open(name, oflag, mode)
        if errno != 0:
            raise RuntimeError(f'create SharedMemory failed! <{os.strerror(errno)}>')
        if oflag & os.O_CREAT:
            self.resize(size)
        self._map_size = 0

    def resize(self, size, strict=False):
        shm_size = self.shm_size
        if shm_size < size or (shm_size > size and strict):
            os.ftruncate(self.fd, size)

    def __remap(self, size):
        self._mmap = mmap.mmap(self.fd, size)
        self._buf = memoryview(self._mmap)
        self._map_size = size

    @property
    def shm_size(self):
        stats = os.fstat(self.fd)
        return stats.st_size

    @property
    def buf(self):
        shm_size = self.shm_size
        if shm_size != self._map_size:
            self.__remap(shm_size)
        return self._buf

del __SharedMemory
