def filter_by_participants(calender, user):
    return sorted(list(filter(lambda x: x.include(user), calender)))

