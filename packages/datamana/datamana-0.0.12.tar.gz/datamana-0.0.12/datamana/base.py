import os, time, pickle
from multiprocessing import shared_memory
from datamana._C import Semaphore, MQueue
from typing import Iterable

class Base():
    def __init__(self, name):
        self.data_name = f'datamana{name}'
        self.data_meta_name = f'{self.data_name}meta'
        self.data_share_name = f'{self.data_name}share'
        self.data_sem_name = f'{self.data_name}sem'
        self.data_mq_tx_name =f'/{self.data_name}mqtx'
        self.data_mq_rx_name =f'/{self.data_name}mqrx'
        self.sem = Semaphore()
        self.mq_tx = MQueue()
        self.mq_rx = MQueue()

    @staticmethod
    def write_shared_data(shm_name, data, size):
        shm_data = shared_memory.SharedMemory(name=shm_name, create=True, size=size)

        if shm_data.size < size:
            shm_data.close()
            shm_data.unlink()
            shm_data = shared_memory.SharedMemory(name=shm_name, create=True, size=size)

        shm_data.buf[:size] = data[:]
        shm_data.close()

    def server_send(self, msg, msg_prio=0):
        return self.mq_tx.send(msg, msg_prio)

    def server_recv(self):
        return self.mq_rx.receive()

    def client_send(self, msg, msg_prio=0):
        return self.mq_rx.send(msg, msg_prio)

    def client_recv(self):
        return self.mq_tx.receive()
