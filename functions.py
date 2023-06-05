def add_time_fields(line):
    time = str(line['frame.time'])
    new_time = convert_time_format_v3(time)
    ts = convert_to_timestamp(time)
    line['time'] = new_time
    line['ts'] = ts
    return new_time


    
from datetime import datetime

def convert_time_format(s):
    # split timestamp and timezone
    timestamp, timezone = s.rsplit(" ", 1)
    # trim fractional seconds to microseconds
    timestamp = timestamp[:timestamp.rindex('.')+7]
    # create datetime object from string
    dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S.%f")
    # create new string from datetime object
    new_s = dt.strftime("%H:%M:%S.%f")
    return new_s

def convert_time_format_v2(s):
    # split timestamp and timezone
    timestamp, timezone = s.rsplit(" ", 1)
    # trim fractional seconds to milliseconds
    timestamp = timestamp[:timestamp.rindex('.')+4]
    # create datetime object from string
    dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S.%f")
    # create new string from datetime object
    new_s = dt.strftime("%b %d, %Y %H:%M:%S.%f")[:-3]
    return new_s

def convert_time_format_v3(s):
    # split timestamp and timezone
    timestamp, timezone = s.rsplit(" ", 1)
    # trim fractional seconds to seconds
    timestamp = timestamp[:timestamp.rindex('.')]
    # create datetime object from string
    dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S")
    # create new string from datetime object
    new_s = dt.strftime("%Y-%m-%d %H:%M:%S")
    return new_s


def convert_to_timestamp(s):
    # split timestamp and timezone
    timestamp, timezone = s.rsplit(" ", 1)
    # trim fractional seconds to seconds
    timestamp = timestamp[:timestamp.rindex('.')]
    # create datetime object from string
    dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S")
    # convert datetime object to timestamp
    ts = dt.timestamp()
    return int(ts)

def convert_to_timestamp_with_ms(s):
    # split timestamp and timezone
    timestamp, timezone = s.rsplit(" ", 1)

    # trim fractional seconds to milliseconds
    timestamp = timestamp[:timestamp.rindex('.')+4]

    # create datetime object from string
    dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S.%f")

    # convert datetime object to timestamp with milliseconds
    ts = round(dt.timestamp(), 3)

    return ts




def get_subscription_data(line):
    # the msisdn and imsi can be in different fields
    if not line.get("diameter.Subscription-Id-Data"):
        return None
    subscription_data = line.get("diameter.Subscription-Id-Data")
    if "," in subscription_data:
        msisdn = subscription_data.split(",")[0]
        imsi = subscription_data.split(",")[1]
        return msisdn, imsi
    else:
        return subscription_data

def get_session_id(line):
    if not line.get("diameter.Session-Id"):
        return None
    return line.get("diameter.Session-Id")

def get_framed_ip(line):
    if not line.get("diameter.Framed-IP-Address"):
        return None
    return line.get("diameter.Framed-IP-Address")

