# Filename: sessions.py
from typing import Any
from diameter_messages import DiameterMessage

class Session():
    def __init__(self, session_id):
        """Initialize a Session object."""
        self.session_id = session_id
        self.start_time = None
        self.end_time = None
        self.messages = []
        self.cluster = None

    def start_session(self, message):
        """Start the session at the given time."""
        start_time = message.time
        self.cluster = message.cluster
        self.start_time = start_time

    def end_session(self, message):
        """End the session at the given time."""
        end_time = message.time
        self.end_time = end_time

    def add_message(self, message):
        """Add a DiameterMessage object to the session."""
        if isinstance(message, DiameterMessage):
            self.messages.append(message)

    def get_messages(self):
        """Return all the messages of the session."""
        return self.messages.sort(key=lambda x: x.time)
    
    def return_tshark_filter(self):
        """Return a tshark filter string based on the session id."""
        return f"(diameter.Session-Id == \"{self.session_id}\")"
    
    def __getattribute__(self, __name: str) -> Any:
        if __name == "tshark_filter":
            return self.return_tshark_filter()
        """Return the attribute of the object."""
        return super().__getattribute__(__name)

pcrf_messages = ["CCA-I", "CCA-U", "CCA-T", "RAR"]
pgw_messages = ["CCR-I", "CCR-U", "CCR-T", "RAA"]

class GxSession(Session):
    def __init__(self, gx_session_id, framed_ip):
        """Initialize a GxSession object."""
        super().__init__(gx_session_id)
        self.framed_ip = framed_ip
        self.rx_sessions = []

    def add_rx_session(self, rx_session):
        """Add a RxSession object to the session."""
        if isinstance(rx_session, RxSession):
            self.rx_sessions.append(rx_session)

    def return_tshark_filter(self):
        """Return a tshark filter string based on the session id and all rx session ids."""
        tshark_filter = f"diameter.Session-Id == \"{self.session_id}\""
        for rx_session in self.rx_sessions:
            tshark_filter += f" || diameter.Session-Id == \"{rx_session.session_id}\""
        return tshark_filter
    
    def check_session_binding(self):
        # check if the first rx session is in the same cluster as the gx session
        if self.cluster is None:
            return None
        if len(self.rx_sessions) == 0:
            return None
        if self.rx_sessions[0].cluster is None:
            return None
        if self.rx_sessions[0].cluster == self.cluster:
            return True
        return False


    def __repr__(self) -> str:
        """Return a string representation of the GxSession object."""
        return f"GxSession(session_id={self.session_id}, start_time={self.start_time}, end_time={self.end_time}, n_messages={len(self.messages)})"
    
    def __getattribute__(self, __name: str) -> Any:
        if __name == "session_binding":
            return self.check_session_binding()
        return super().__getattribute__(__name)
    

class RxSession(Session):
    def __init__(self, rx_session_id, gx_session, subscriber_id):
        """Initialize a RxSession object."""
        super().__init__(rx_session_id)
        self.gx_session = gx_session
        self.gx_session_id = gx_session.session_id
        self.subscriber_id = subscriber_id

    def add_message(self, message):
        """Add a DiameterMessage object to the session."""
        if isinstance(message, DiameterMessage):
            self.messages.append(message)
            self.gx_session.add_message(message)

    def is_voice_call(self):
        """Return True if the session contains a voice call."""
        for message in self.messages:
            if message.is_voice_call():
                return True
        return False
    
    def get_end_time(self):
        """Return the end time of the session."""
        if self.end_time:
            return self.end_time
        else:
            if len(self.messages) == 0:
                return None
            return self.messages[-1].time
        
    def get_duration(self):
        """Return the duration of the session."""
        if self.start_time and self.end_time:
            return float(self.end_time) - float(self.start_time)
        else:
            return None

    def __repr__(self) -> str:
        """Return a string representation of the RxSession object."""
        if not self.is_voice_call():
            return f"RxSession(session_id={self.session_id}, duration={self.get_duration()}s, start_time={self.start_time}, end_time={self.end_time}, n_messages={len(self.messages)}, gx_session_id={self.gx_session_id})"
        return f"VoiceCall(start_time={self.start_time}, end_time={self.end_time}, duration={self.get_duration()}s, n_messages={len(self.messages)}, gx_session_id={self.gx_session_id})"
    


class RxSessions:
    def __init__(self, gx_sessions=None):
        self.sessions = {}
        self.gx_sessions = gx_sessions

    def add_session(self, rx_session):
        self.sessions[rx_session.session_id] = rx_session
    
    def get_session_by_session_id(self, rx_session_id):
        return self.sessions.get(rx_session_id)
    
    def get_subscriber_sessions(self, msisdn):
        subscriber_sessions = []
        # get all rx sessions
        for session in self.sessions.values():
            if session.subscriber_id == msisdn:
                subscriber_sessions.append(session)
        return subscriber_sessions
    
        


class GxSessions:
    def __init__(self, subscribers, rx_sessions=None):
        self.sessions = {}
        self.subscribers = subscribers
        self.rx_sessions = rx_sessions

    def add_session(self, subscriber, gx_session):
        if not self.sessions.get(subscriber):
            self.sessions[subscriber] = []
        self.sessions[subscriber].append(gx_session)
        # add gx session to subscriber
        subscriber.add_gx_session(gx_session)


    def get_subscriber_by_session_id(self, session_id):
        for subscriber, gx_session_list in self.sessions.items():
            for gx_session in gx_session_list:
                if gx_session.session_id == session_id:
                    return subscriber
        return None
    
    def get_session_by_session_id(self, session_id):
        for subscriber, gx_session_list in self.sessions.items():
            for gx_session in gx_session_list:
                if gx_session.session_id == session_id:
                    return gx_session
        return None
    
    def get_subscriber_by_framed_ip(self, framed_ip):
        for subscriber, gx_session_list in self.sessions.items():
            for gx_session in gx_session_list:
                if gx_session.framed_ip == framed_ip:
                    return subscriber
        return None
    
    def get_session_by_framed_ip(self, framed_ip):
        for subscriber, gx_session_list in self.sessions.items():
            for gx_session in gx_session_list:
                if gx_session.framed_ip == framed_ip:
                    return gx_session
        return None
    
    def get_subscriber_sessions(self, msisdn):
        subscriber_sessions = []
        for subscriber, gx_session_list in self.sessions.items():
            if subscriber.msisdn == msisdn:
                for gx_session in gx_session_list:
                    subscriber_sessions.append(gx_session)
        return subscriber_sessions
    
