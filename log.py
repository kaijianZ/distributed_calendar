class Meeting(object):
    def __init__(self, name, day, start, end, participants):
        self.name = name
        self.day = day
        self.start = start
        self.end = end
        self.participants = participants

    def include(self, user):
        return user in self.participants

    def conflict(self, other_meeting):
        pass

    def __str__(self):
        str_participants = self.participants[0]
        for user in self.participants[1:]:
            str_participants += ',' + user
        return self.name + ' ' + self.day.strftime(
            "%m/%d/%Y") + ' ' + self.start.isoformat(
            timespec='minutes') + ' ' + self.end.isoformat(
            timespec='minutes') + ' ' + str_participants


class Log(object):
    pass
