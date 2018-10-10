def filter_by_participants(calender, user):
    return list(filter(lambda x: x.include(user), calender))


def sorted_view(calender):
    return sorted(calender, key=lambda x: (x.day.strftime("%m/%d/%Y"),
                                           x.start.isoformat(
                                               timespec='minutes'),
                                           x.name))
