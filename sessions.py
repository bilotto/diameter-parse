# Filename: sessions.py
from typing import Any
from diameter_messages import DiameterMessage
from mylog import logging

class Session():
    def __init__(self, session_id):
        """Initialize a Session object."""
        self.session_id = session_id
        self.start_time = None
        self.end_time = None
        self.messages = []
        self.host = None
        self.messages_pairs_tuples = []

    def start_session(self, message):
        """Start the session at the given time."""
        start_time = message.time
        self.host = message.to_host
        self.start_time = start_time

    def end_session(self, message):
        """End the session at the given time."""
        end_time = message.time
        self.end_time = end_time
            
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
    
    def get_message_by_name(self, message_name):
        """Return the first message with the given name."""
        for message in self.messages:
            if message.message_name == message_name:
                return message
        return None


class GxSession(Session):
    def __init__(self, gx_session_id, framed_ip):
        """Initialize a GxSession object."""
        super().__init__(gx_session_id)
        self.framed_ip = framed_ip
        self.rx_sessions = []
        # gx session fields
        self.rat_type = None
        self.ip_can_type = None

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
    
    def add_message(self, message):
        """Add a DiameterMessage object to the session."""
        if isinstance(message, DiameterMessage):
            self.messages.append(message)
            # add message to the messages pairs list
            # requests messages will always be first in the tuple
            if message.is_request():
                messages_pair = (message, None)
                self.messages_pairs_tuples.append(messages_pair)
            elif message.message_name == "CCA-I" or message.message_name == "CCA-U" or message.message_name == "CCA-T":
                for i in range(len(self.messages_pairs_tuples)):
                    if self.messages_pairs_tuples[i][0].get_avp("CC-Request-Number") == message.get_avp("CC-Request-Number"):
                        # Add to the same tuple
                        self.messages_pairs_tuples[i] = (self.messages_pairs_tuples[i][0], message)
                        break
            elif message.message_name == "RAA":
                # RAA messages are paired to RAR, but there is no field to match them, it has to be done by order of arrival and/or time
                # find the first RAR message without a RAA message
                for i in range(len(self.messages_pairs_tuples)):
                    if self.messages_pairs_tuples[i][0].message_name == "RAR" and self.messages_pairs_tuples[i][1] is None:
                        self.messages_pairs_tuples[i] = (self.messages_pairs_tuples[i][0], message)
                        break
            elif message.message_name == "AAA":
                # AAA messages are paired to AAR, but there is no field to match them, it has to be done by order of arrival and/or time
                # find the first AAR message without a AAA message
                for i in range(len(self.messages_pairs_tuples)):
                    if self.messages_pairs_tuples[i][0].message_name == "AAR" and self.messages_pairs_tuples[i][1] is None:
                        self.messages_pairs_tuples[i] = (self.messages_pairs_tuples[i][0], message)
                        break
            elif message.message_name == "STA":
                # STA messages are paired to STR, but there is no field to match them, it has to be done by order of arrival and/or time
                # find the first STR message without a STA message
                for i in range(len(self.messages_pairs_tuples)):
                    if self.messages_pairs_tuples[i][0].message_name == "STR" and self.messages_pairs_tuples[i][1] is None:
                        self.messages_pairs_tuples[i] = (self.messages_pairs_tuples[i][0], message)
                        break
            elif message.message_name == "ASA":
                # ASA messages are paired to ASR, but there is no field to match them, it has to be done by order of arrival and/or time
                # find the first ASR message without a ASA message
                for i in range(len(self.messages_pairs_tuples)):
                    if self.messages_pairs_tuples[i][0].message_name == "ASR" and self.messages_pairs_tuples[i][1] is None:
                        self.messages_pairs_tuples[i] = (self.messages_pairs_tuples[i][0], message)
                        break



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
    
