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

