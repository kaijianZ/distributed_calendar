# -*- coding: utf-8 -*-
import asyncio
from aioconsole import ainput
from helper import *
from log import *
from datetime import date, time, datetime


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
        line = await ainput()
        async with lock:
            global calender
            global node
            global counter
            global matrix_clock
            global log
            if line == 'view':
                for meeting in sorted_view(calender.values()):
                    print(meeting)
            elif line == 'myview':
                for meeting in sorted_view(filter_by_participants(
                        calender.values(), node)):
                    print(meeting)
            else:
                line = line.split(' ')
                if line[0] == 'schedule':
                    line = line[1:]
                    name = line[0]
                    day = datetime.strptime(line[1], "%m/%d/%Y").date()
                    start = datetime.strptime(line[2], "%I:%M").time()
                    end = datetime.strptime(line[3], "%I:%M").time()
                    participants = line[4].split(',')
                    new_meeting = Meeting(name, day, start, end, participants)
                    if ok_to_schedule(calender.values(), new_meeting):
                        calender[name] = new_meeting
                        counter += 1
                        print('Meeting', name, 'scheduled.')
                    else:
                        print('Unable to schedule meeting', name + '.')
                elif line[0] == 'cancel':
                    name  = line[1]
                    # when the user is the only one in the event
                    if name not in calender:
                        print("nah")
                    else:
                        # deletes the event in the schedule
                        del calender[name]
                        counter += 1
                        # add the deletion to log
                        # log +=
                        # output
                        print(f'Meeting {name} cancelled.')




if __name__ == "__main__": 
    calender = {}
    matrix_clock = []
    counter = 0
    logs = []
    node = 'user1'

    # schedule Breakfast 10/14/2018 08:00 09:00 user1,user2
    # schedule Conference 10/16/2018 12:00 1:30 user1

    lock = asyncio.Lock()
    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        CalenderServerProtocol, local_addr=('127.0.0.1', 9999))
    tasks = [hello(), listen]
    loop.run_until_complete(asyncio.wait(tasks))
