def format_timedelta(td):
    days = td.days
    td_sec = td.seconds
    hours, rem = divmod(td_sec, 3600)
    minuts, seconds = divmod(rem, 60)
    return f'{days} days, {hours:02}:{minuts:02}:{seconds:02}'
