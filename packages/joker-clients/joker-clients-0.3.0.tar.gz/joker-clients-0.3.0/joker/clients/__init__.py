__version__ = "0.3.0"

from joker.clients.cas import ContentAddressedStorageClient
from joker.clients.files import FileStorageInterface
from joker.clients.monolog import MonologInterface
from joker.clients.printable import PrintableClient

CASClient = ContentAddressedStorageClient

if __name__ == "__main__":
    print(__version__)
