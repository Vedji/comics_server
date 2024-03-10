import logging


class BDError(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)
        logging.warning(msg)


class BDErrorItemExists(BDError):
    pass


class BDErrorInitFile(BDError):
    pass
