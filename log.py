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


class Log(object):
    pass
