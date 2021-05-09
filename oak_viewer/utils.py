

def format_time_str(time_s):
    """ Format time in seconds to timestring in HH:MM:SS format
    """
    time_s = int(time_s)
    m, s = divmod(time_s, 60)
    h, m = divmod(m, 60)
    time_str = '{:d} : {:02d} : {:02d}'.format(h, m, s)

    return time_str
