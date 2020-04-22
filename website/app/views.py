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
browsers = []
servers = []

def index(request):
    return render(request, "index.html")


# action is receive, can be found by others
def receive(request):
    server = AirDropServer(config)
    servers.append(server)
    _start_receive(server)
    return HttpResponse(status=200)

def receive_close(request):
    if servers[0]:
        servers[0].stop()

    return HttpResponse(status=200)


def find(request):
    browser = AirDropBrowser(config)
    browsers.append(browser)
    find_users = []
    browser.start(callback_add=_found_receiver)

    # TODO: render to device list page.
    # TODO: can send request every one second to retrieve the find_users list
    #       from the frontend json file.
    return redirect(reverse("find_list"))


def find_stop(request):
    if browsers[0]:
        browsers[0].stop()

    return HttpResponse(find_users)

def find_list(request):
    # render to device list page.
    # TODO: can send request every one second to retrieve the find_users list
    #       from the frontend json file.
    context = {"devices": find_users}
    return render(request, 'devices.json', context, content_type='application/json')

def send(request):
    pass


def _start_receive(server):
    thread = threading.Thread(target= _receive_service, args=(server, ))
    thread.start()

def _receive_service(server):
    server.start_service()
    server.start_server()

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
        if receiver_name not in find_users:
            find_users.append(receiver_name)
    else:
        res = 'Receiver ID {} is not discoverable'.format(id)

    lock.release()
