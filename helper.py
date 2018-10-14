import pickle
import socket
from log import *


def filter_by_participants(calender, user):
    return list(filter(lambda x: x.include(user), list(calender)))


def sorted_view(calender):
    return sorted(list(calender), key=lambda x: (x.date.strftime("%m/%d/%Y"),
                                                 x.start.isoformat(
                                                     timespec='minutes'),
                                                 x.name))


def ok_to_schedule(calender, meeting):
    participants = meeting.participants
    for user in participants:
        schedule = filter_by_participants(calender, user)
        for s in schedule:
            if meeting.conflict(s):
                return False
    return True


def host_to_num(host_list):
    host_to_num = {}
    host_list.sort()
    for i, ele in enumerate(host_list):
        host_to_num[ele] = i
    return host_to_num


def send_log(matrix_clock, logs, host, port, host_num_dict):
    host_num = host_num_dict[host]
    sending_logs = list(filter(lambda rec: not has_rec(matrix_clock, rec,
                                                       host_num), logs))
    sending_logs = pickle.dumps((matrix_clock, sending_logs))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(sending_logs, (host, port))
    s.close()


def has_rec(t, log, host_num):
    return t[host_num][log.node] >= log.time


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
    for host in participants:
        if host != this_node:
            send_log(t_i, logs, host, hosts[host],
                     host_num_dict)
    print(f'Meeting {name} cancelled.')
