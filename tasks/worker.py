from utils.connection import REDIS
from rq.worker import Worker
from rq import Queue, Connection
from typing import Optional, Union


def run_worker(queues: Optional[list[str]] = None):
    queues = queues if queues else ["single", "dual", "chat"]

    with Connection(REDIS):
        worker = Worker(map(Queue, queues))
        worker.work()
