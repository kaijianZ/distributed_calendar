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


def host_by_num(host_list):
    host_by_num = {}
    host_list.sort()
    for ind in range(len(host_list)):
        host_by_num[ind] = [host_list[ind]]
    return host_by_num
