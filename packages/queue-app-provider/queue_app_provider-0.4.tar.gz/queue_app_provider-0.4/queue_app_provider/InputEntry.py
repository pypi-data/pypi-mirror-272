import os
import tempfile
from typing import Callable

from werkzeug.datastructures import FileStorage

# Very simple class, an InputEntry is just a holder for queue entries in our
# processing system.
#
# Since we are working with files, this InputEntry receives a `FileStorage`
# object from the flask request, and dumps original file object to
# a local file. When queue process this entry, handler is called and
# after that the local file is purged from system
#
# Created by: David Rodríguez Alfayate
# Version: 1.0
from queue_app_provider.HandlerOutput import HandlerOutput
import logging

logger = logging.getLogger('queue-app-provider:input-entry')


class InputEntry:
    def __init__(self, file_storage: FileStorage, callback):
        self.callback = callback
        self.fh, self.file = tempfile.mkstemp()
        logger.debug('Storing temporary file in %r', self.file)
        file_storage.save(self.file)

    # Temporary file removal
    def clear(self):
        os.close(self.fh)
        os.remove(self.file)

    # Data processing function called from `QueueThread` main queue
    # we just execute the handler method
    def handle(self, handler: Callable[[str], HandlerOutput]):
        # We process input, sending response to external
        # processing system
        output = handler(self.file)
        try:
            logger.debug('Handler result is %r', output)
            output.notify(self.callback)
        finally:
            self.clear()
