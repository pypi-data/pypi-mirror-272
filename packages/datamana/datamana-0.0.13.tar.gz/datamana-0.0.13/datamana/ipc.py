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
        super().__init__()
        name = '/' + name
        errno = self.open(name, oflag, mode)
        if errno != 0:
            raise RuntimeError(f'create SharedMemory failed! <{os.strerror(errno)}>')
        self.resize(size)

    def resize(self, size, strict=False):
        shm_size = self.size
        if shm_size < size or (shm_size > size and strict):
            os.ftruncate(self.fd, size)
            shm_size = size
            self._mmap = mmap.mmap(self.fd, size)
            self._buf = memoryview(self._mmap)

    @property
    def size(self):
        stats = os.fstat(self.fd)
        shm_size = stats.st_size
        return shm_size

    @property
    def buf(self):
        return self._buf

del __SharedMemory
