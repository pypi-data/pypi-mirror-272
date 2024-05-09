from datamana.ipc import Semaphore, MQueue, SharedMemory

class Base():
    def __init__(self, name):
        self.data_name = f'datamana{name}'
        self.data_meta_name = f'{self.data_name}meta'
        self.data_share_name = f'{self.data_name}share'
        self.data_sem_name = f'{self.data_name}sem'
        self.data_mq_tx_name =f'{self.data_name}mqtx'
        self.data_mq_rx_name =f'{self.data_name}mqrx'
        self.sem = Semaphore(self.data_sem_name)
        self.mq_tx = MQueue(self.data_mq_tx_name)
        self.mq_rx = MQueue(self.data_mq_rx_name)
        self.name2shm = {}

    def write_shared_data(self, shm_name, data, size):
        if shm_name in self.name2shm:
            shm = self.name2shm[shm_name]
        else:
            shm = SharedMemory(name=shm_name, size=size)
            self.name2shm[shm_name] = shm
        shm.resize(size)

        shm.buf[:size] = data[:]

    def server_send(self, msg, msg_prio=0):
        return self.mq_tx.send(msg, msg_prio)

    def server_recv(self):
        return self.mq_rx.receive()

    def client_send(self, msg, msg_prio=0):
        return self.mq_rx.send(msg, msg_prio)

    def client_recv(self):
        return self.mq_tx.receive()
