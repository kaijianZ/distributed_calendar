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

def send(pl, listHasNoRec):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for index in enumerate(hasNoRec):
        siteaddr = listHasNoRec[index][0]
        siteport = listHasNoRec[index][1]
        s.sendto(pl, (siteaddr, siteport))
    s.close()

def hasRec(pl)