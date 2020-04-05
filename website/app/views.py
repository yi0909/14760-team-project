from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.opendropConfig import AirDropConfig, AirDropReceiverFlags
from app.opendropServer import AirDropServer
from app.opendropClient import AirDropBrowser, AirDropClient

import threading
import requests

find_users = []
config = AirDropConfig()
discover = []
lock = threading.Lock()
browser = AirDropBrowser(config)

def index(request):
    return HttpResponse("open drop")


# action is receive
def receive(request):
    server = AirDropServer(config)
    server.start_service()
    server.start_server()
    pass

def find(request):
    find_users = []
    browser.start(callback_add=_found_receiver)

    # TODO: render to device list page.
    # TODO: can send request every one second to retrieve the find_users list
    #       from the frontend json file.
    return redirect(reverse("find_list"))


def find_stop(request):
    browser.stop()

    return HttpResponse(find_users)

def find_list(request):
    print("find_list")
    # TODO: render to device list page.
    # TODO: can send request every one second to retrieve the find_users list
    #       from the frontend json file.
    context = {}
    return render(request, 'index.html', context)

def send(request):
    pass


def _found_receiver(info):
    thread = threading.Thread(target=_send_discover, args=(info, ))
    thread.start()


def _send_discover(info):
    try:
        address = info.parsed_addresses()[0]  # there should only be one address
    except IndexError:
        # logger.warn('Ignoring receiver with missing address {}'.format(info))
        return
    id = info.name.split('.')[0]
    hostname = info.server
    port = int(info.port)
    # logger.debug('AirDrop service found: {}, {}:{}, ID {}'.format(hostname, address, port, id))
    client = AirDropClient(config, (address, int(port)))
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

    index = len(discover)
    node_info = {
        'name': receiver_name,
        'address': address,
        'port': port,
        'id': id,
        'flags': flags,
        'discoverable': discoverable,
    }
    lock.acquire()
    discover.append(node_info)
    if discoverable:
        res = 'Found  index {}  ID {}  name {}'.format(index, id, receiver_name)
        find_users.append(res)
        print(res)
    else:
        res = 'Receiver ID {} is not discoverable'.format(id)
        find_users.append(res)
    lock.release()
