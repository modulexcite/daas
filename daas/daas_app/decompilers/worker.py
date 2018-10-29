from .decompiler_factory import DecompilerCreator
from .utils import send_result


# This function should by called by redis queue (rq command).
def worker(task):
    send_result(DecompilerCreator().create(task['config']).process(task['sample']))
