from datetime import timedelta

from timeloop import Timeloop

from frontpy_core.dev.resources_indexer import ResourcesIndexer


def launch_dev_worker(app_root_dir):
    tl = Timeloop()

    indexer = ResourcesIndexer(app_root_dir)
    tl.job(interval=timedelta(seconds=10))(indexer.reindex)

    tl.start(block=True)
