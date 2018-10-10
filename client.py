# -*- coding: utf-8 -*-
import asyncio
from aioconsole import ainput


class CalenderServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)


async def hello():
    while True:
        line = await ainput('>>> ')
        print(line)


if __name__ == "__main__":
    calender = []
    matrix_clock = []
    counter = 0
    logs = []

    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        CalenderServerProtocol, local_addr=('127.0.0.1', 9999))
    tasks = [hello(), listen]
    loop.run_until_complete(asyncio.wait(tasks))
