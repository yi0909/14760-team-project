from django.http import HttpResponse
from app.opendropConfig import AirDropConfig, AirDropReceiverFlags
from app.opendropServer import AirDropServer
from app.opendropClient import AirDropBrowser, AirDropClient

import threading

find_users = []

def index(request):
    return HttpResponse("open drop")


# action is receive
def receive(request):
    config = AirDropConfig()
    server = AirDropServer(config)
    server.start_service()
    server.start_server()
    pass

def find(request):
    config = AirDropConfig()
    browser = AirDropBrowser(config)
    browser.start(callback_add=_found_receiver)

    # TODO: render to device list page.
    # TODO: can send request every one second to retrieve the find_users list
    #       from the frontend json file.
    return HttpResponse("to implement find")

def send(request):
    pass


def _found_receiver(self, info):
    print("found receiver")
    thread = threading.Thread(target=_send_discover, args=(info, ))
    thread.start()


def _send_discover(self, info):
    try:
        address = info.parsed_addresses()[0]  # there should only be one address
    except IndexError:
        # logger.warn('Ignoring receiver with missing address {}'.format(info))
        return
    id = info.name.split('.')[0]
    hostname = info.server
    port = int(info.port)
    # logger.debug('AirDrop service found: {}, {}:{}, ID {}'.format(hostname, address, port, id))
    client = AirDropClient(self.config, (address, int(port)))
    try:
        flags = int(info.properties[b'flags'])
    except KeyError:
        # TODO in some cases, `flags` are not set in service info; for now we'll try anyway
        flags = AirDropReceiverFlags.SUPPORTS_DISCOVER_MAYBE

    if flags & AirDropReceiverFlags.SUPPORTS_DISCOVER_MAYBE:
        try:
            receiver_name = client.send_discover()
        except TimeoutError:
            receiver_name = None
    else:
        receiver_name = None
    discoverable = receiver_name is not None

    index = len(self.discover)
    node_info = {
        'name': receiver_name,
        'address': address,
        'port': port,
        'id': id,
        'flags': flags,
        'discoverable': discoverable,
    }
    self.lock.acquire()
    self.discover.append(node_info)
    if discoverable:
        res = 'Found  index {}  ID {}  name {}'.format(index, id, receiver_name)
        find_users.append(res)
    else:
        res = 'Receiver ID {} is not discoverable'.format(id)
        find_users.append(res)
    self.lock.release()
