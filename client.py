# -*- coding: utf-8 -*-
import asyncio
from aioconsole import ainput
from helper import *
from log import *
from datetime import date, time, datetime
import sys
import pickle


def delete(name):
    global calender
    global this_node
    global counter
    global t_i
    global logs
    global hosts
    global host_num_dict
    participants = calender[name].participants
    del calender[name]
    counter += 1
    t_i[host_num_dict[this_node]][host_num_dict[this_node]] = counter
    new_log = Log('delete', counter, host_num_dict[this_node], name)
    logs.append(new_log)
    notify(participants, this_node, t_i, logs, hosts, host_num_dict)
    print(f'Meeting {name} cancelled.')


class CalenderServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        global calender
        global this_node
        global counter
        global t_i
        global logs
        global hosts
        global host_num_dict
        k = host_num_dict[addr[0]]
        i = host_num_dict[this_node]
        t_k, NP = pickle.loads(data)
        NE = list(filter(lambda rec: not has_rec(t_i, rec,
                                                 i), NP))
        insert_set = set()
        delete_set = set()
        for l in NE:
            if l.op == 'delete':
                delete_set.add(l.value)
            else:
                insert_set.add(l.value)

        waiting_delete = set()

        for insert_meeting in insert_set:
            if insert_meeting.name not in delete_set:
                for meeting in sorted_view(filter_by_participants(
                        calender.values(), this_node)):
                    if insert_meeting.conflict(meeting) and \
                            insert_meeting.name > meeting.name:
                        waiting_delete.add(insert_meeting.name)
                        continue
                    elif insert_meeting.conflict(meeting) and meeting.name \
                            not in delete_set:
                        waiting_delete.add(meeting.name)
                calender[insert_meeting.name] = insert_meeting

        for delete_meeting in delete_set:
            if delete_meeting in calender:
                del calender[delete_meeting]

        for r in range(len(hosts)):
            t_i[i][r] = max(t_i[i][r], t_k[k][r])

        for r in range(len(hosts)):
            for s in range(len(hosts)):
                t_i[r][s] = max(t_i[r][s], t_k[r][s])

        for l in NE:
            if l not in logs:
                for s in range(len(hosts)):
                    if not has_rec(t_i, l, s):
                        logs.append(l)
                else:
                    continue

        for name in waiting_delete:
            delete(name)


async def console_input():
    while True:
        line = await ainput()

        global calender
        global this_node
        global counter
        global t_i
        global logs
        global hosts
        global host_num_dict
        if line == 'view':
            for meeting in sorted_view(calender.values()):
                print(meeting)

        elif line == 'myview':
            for meeting in sorted_view(filter_by_participants(
                    calender.values(), this_node)):
                print(meeting)

        elif line == 'log':
            for l in logs:
                print(l)

        else:
            line = line.split(' ')

            if line[0] == 'schedule':
                line = line[1:]
                name = line[0]
                day = datetime.strptime(line[1], "%m/%d/%Y").date()
                start = datetime.strptime(line[2], "%H:%M").time()
                end = datetime.strptime(line[3], "%H:%M").time()
                participants = line[4].split(',')

                new_meeting = Meeting(name, day, start, end, participants)

                if ok_to_schedule(calender.values(), new_meeting):
                    calender[name] = new_meeting
                    counter += 1
                    t_i[host_num_dict[this_node]][
                        host_num_dict[this_node]] = counter
                    new_log = Log('create', counter, host_num_dict[this_node],
                                  new_meeting)
                    logs.append(new_log)
                    print('Meeting', name, 'scheduled.')
                    notify(participants, this_node, t_i, logs, hosts,
                           host_num_dict)

                else:
                    print('Unable to schedule meeting', name + '.')

            elif line[0] == 'cancel':
                name = line[1]
                # when the user is the only one in the event
                if name not in calender:
                    print("nah")

                else:
                    # deletes the event in the schedule
                    delete(name)


if __name__ == "__main__":

    # schedule Breakfast 10/14/2018 08:00 09:00 192.168.0.7,192.168.0.21
    # schedule Conference 10/16/2018 12:00 13:30 192.168.0.7

    this_node = sys.argv[1]
    hosts = {}

    with open('knownhosts_udp.txt', 'r') as f:
        for line in f.readlines():
            if len(line) != 0:
                line = line.strip('\n')
                line = line.split(' ')
                hosts[line[0]] = int(line[1])
    port = hosts[this_node]
    host_num_dict = host_to_num(list(hosts.keys()))

    # variables that can be persisted
    t_i = [[0 for _ in range(len(hosts))] for _ in range(len(hosts))]
    calender = {}
    counter = 0
    logs = []

    loop = asyncio.get_event_loop()
    print("Starting UDP server")
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        CalenderServerProtocol, local_addr=(this_node, port))
    tasks = [console_input(), listen]
    loop.run_until_complete(asyncio.wait(tasks))
