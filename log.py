class Meeting(object):
    def __init__(self, name, date, start, end, participants):
        self.name = name
        self.date = date
        self.start = start
        self.end = end
        self.participants = participants

    def include(self, user):
        return user in self.participants

    def conflict(self, other_meeting):
        return other_meeting.date == self.date and \
               (self.start < other_meeting.end <= self.end or
                self.start <= other_meeting.start < self.end or
                other_meeting.start < self.end <= other_meeting.end or
                other_meeting.start <= self.start < other_meeting.end)

    def __str__(self):
        str_participants = self.participants[0]
        for user in self.participants[1:]:
            str_participants += ',' + user
        return self.name + ' ' + self.date.strftime(
            "%m/%d/%Y") + ' ' + self.start.isoformat(
            timespec='minutes') + ' ' + self.end.isoformat(
            timespec='minutes') + ' ' + str_participants


class Log(object):
    def __init__(self, op, time, node, value):
        self.op = op
        self.time = time
        self.node = node
        self.value = value

    def __str__(self):
        return self.op + ' ' + str(self.value)
