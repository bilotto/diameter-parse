class Subscriber:
    def __init__(self, msisdn, imsi):
        self.msisdn = msisdn
        self.imsi = imsi
        # Suscriber session info
        self.gx_session_id = None
        self.rx_session_id = None
        self.framed_ip = None
        # Subscriber sessions
        self.gx_sessions = []

    def add_gx_session(self, gx_session):
        self.gx_sessions.append(gx_session)

    def set_gx_session_id(self, session_id):
        self.gx_session_id = session_id

    def set_rx_session_id(self, session_id):
        self.rx_session_id = session_id

    def set_framed_ip(self, framed_ip):
        self.framed_ip = framed_ip

    def set_gx_sessions(self, gx_sessions):
        self.gx_sessions = gx_sessions

    def set_rx_sessions(self, rx_sessions):
        self.rx_sessions = rx_sessions

    def __repr__(self) -> str:
        return f"{self.msisdn}"

from mylog import logging

class Subscribers(dict):
    def __init__(self):
        self.subscribers = {}
        self.framed_ips = {}
        self.gx_sessions = {}
        self.rx_sessions = {}

    def get_gx_session(self, gx_session_id):
        return self.gx_sessions.get(gx_session_id)
    
    def get_rx_session(self, rx_session_id):
        return self.rx_sessions.get(rx_session_id)
    
    def add_gx_session(self, gx_session_id, subscriber):
        self.gx_sessions[gx_session_id] = subscriber
        subscriber.set_gx_session_id(gx_session_id)

    def add_rx_session(self, rx_session_id, subscriber):
        self.rx_sessions[rx_session_id] = subscriber
        subscriber.set_rx_session_id(rx_session_id)

    def remove_rx_session(self, rx_session_id, subscriber, error=False):
        if not self.rx_sessions.get(rx_session_id):
            logging.error(f"Rx session {rx_session_id} not found")
            return
        self.rx_sessions.pop(rx_session_id)
        subscriber.set_rx_session_id(None)
        if not error:
            logging.info(f"{subscriber.msisdn},Rx session {rx_session_id} closed")
        else:
            logging.error(f"{subscriber.msisdn},Rx session {rx_session_id} not opened")

    def remove_gx_session(self, gx_session_id, subscriber):
        if not self.gx_sessions.get(gx_session_id):
            logging.error(f"Gx session {gx_session_id} not found")
            return
        self.gx_sessions.pop(gx_session_id)
        subscriber.set_gx_session_id(None)
        subscriber.set_framed_ip(None)
        logging.info(f"{subscriber.msisdn},Gx session {gx_session_id} closed")

    def add_framed_ip(self, framed_ip, subscriber):
        self.framed_ips[framed_ip] = subscriber
        subscriber.set_framed_ip(framed_ip)

    def add_subscriber(self, subscriber):
        if not isinstance(subscriber, Subscriber):
            raise TypeError("Input must be a Subscriber object")
        if self.subscribers.get(subscriber.msisdn):
            # print(f"Subscriber {subscriber.msisdn} already exists")
            return
        logging.debug(f"Adding Subscriber({subscriber.msisdn},{subscriber.imsi})")
        self.subscribers[subscriber.msisdn] = subscriber

    def get_subscribers(self):
        return self.subscribers.values()


    def __repr__(self) -> str:
        # Return json format of the subscribers
        return str(self.subscribers)

    def get_subscriber(self, msisdn):
        return self.subscribers.get(msisdn)

    def get_subscriber_new(self, msisdn_or_imsi, session_id, framed_ip):
        # first try to get subscriber using msisdn, then using session id, then using framed ip
        if msisdn_or_imsi:
            for subscriber in self.subscribers.values():
                if subscriber.msisdn == msisdn_or_imsi:
                    logging.debug(f"Subscriber found using msisdn {msisdn_or_imsi}")
                    return subscriber
                elif subscriber.imsi == msisdn_or_imsi:
                    logging.debug(f"Subscriber found using imsi {msisdn_or_imsi}")
                    return subscriber
        elif session_id:
            # first try to look in gx sessions id, then in rx sessions ids
            for subscriber in self.subscribers.values():
                if subscriber.gx_sessions.get_session(session_id):
                    logging.debug(f"Subscriber found using gx session id {session_id}")
                    return subscriber
                elif subscriber.gx_sessions.get_by_rx_session_id(session_id):
                    logging.debug(f"Subscriber found using rx session id {session_id}")
                    return subscriber
        for subscriber in self.subscribers.values():
            if subscriber.gx_sessions.get_by_framed_ip(framed_ip):
                logging.debug(f"Subscriber found using framed ip {framed_ip}")
                return subscriber
        return None

    def parse_ccr_i(self, line, subscriber):
        time = line.get("time")
        if subscriber.gx_session_id:
            logging.warning(f"{time},{subscriber.msisdn},Gx Session ID changing from {subscriber.gx_session_id} to {line.get('diameter.Session-Id')}")
        self.add_gx_session(line.get("diameter.Session-Id"), subscriber)
        if subscriber.framed_ip:
            logging.warning(f"{time},{subscriber.msisdn},Framed IP changing from {subscriber.framed_ip} to {line.get('diameter.Framed-IP-Address')}")
        self.add_framed_ip(line.get("diameter.Framed-IP-Address"), subscriber)

    def parse_aar(self, line, subscriber):
        self.add_rx_session(line.get("diameter.Session-Id"), subscriber)

    def parse_aaa(self, line, subscriber):
        time = line.get("time")
        result_code = line.get("diameter.Result-Code")
        if result_code != "2001":
            self.remove_rx_session(line.get("diameter.Session-Id"), subscriber, error=True)

    def parse_str(self, line, subscriber):
        time = line.get("time")
        if not self.get_rx_session(line.get("diameter.Session-Id")):
            logging.error(f"{time},{subscriber.msisdn},STR with no previous Rx session {line.get('diameter.Session-Id')}")
            return
        self.remove_rx_session(line.get("diameter.Session-Id"), subscriber)

    def parse_ccr_t(self, line, subscriber):
        time = line.get("time")
        if not self.get_gx_session(line.get("diameter.Session-Id")):
            logging.error(f"{time},{subscriber.msisdn},CCR-T with no previous Gx session {line.get('diameter.Session-Id')}")
            return
        self.remove_gx_session(line.get("diameter.Session-Id"), subscriber)
        # self.terminate_gx_session(subscriber, line)

#pospago
# subscriber1 = Subscriber("56950018795", "730030540816229")
# subscriber2 = Subscriber("56986124800", "730030540816203")
# #prepago
# subscriber3 = Subscriber("56973401557", "730030540816207")
# subscriber4 = Subscriber("56973179039", "730030540816206")
