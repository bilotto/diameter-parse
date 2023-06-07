import subprocess
from tshark_command import TsharkCommand
from mylog import logging
from avp_values import avp_values
from sessions import GxSession, RxSession, RxSessions, GxSessions
from functions import *
from diameter_messages import *
from subscriber import Subscriber, Subscribers
from diameter_messages import DiameterMessage
from diameter_messages import base_filter, all_fields, diameter_fields
import json

def identify_subscriber(message, subscribers, gx_sessions, rx_sessions):
    diameter_message = DiameterMessage(message)
    diameter_message_name = diameter_message.message_name
    if diameter_message_name == "CCR-I":
        # in the ccri, we get the subscriber from the msisdn
        msisdn, imsi = get_subscription_data(diameter_message.message)
        subscriber = subscribers.get_subscriber(msisdn)
    elif diameter_message_name == "AAR":
        # in the aar, we get the subscriber from the framed_ip address used in the ccri
        session_id = diameter_message.get_avp("Session-Id")
        rx_session = rx_sessions.get_session_by_session_id(session_id)
        if not rx_session:
            framed_ip = diameter_message.get_avp("Framed-IP-Address")
            subscriber = gx_sessions.get_subscriber_by_framed_ip(framed_ip)
        else:
            return None
    else:
        # get the subscriber through the gx session id
        session_id = diameter_message.get_avp("Session-Id")
        subscriber = gx_sessions.get_subscriber_by_session_id(session_id)
    
    return subscriber



def parse_tshark_output(tshark_output, subscribers):
    rx_sessions = RxSessions()
    gx_sessions = GxSessions(subscribers, rx_sessions)
    
    for message in tshark_output:
        diameter_message = DiameterMessage(message)
        diameter_message_name = diameter_message.message_name
        if diameter_message_name == "CCR-I":
            # in the ccri, we get the subscriber from the msisdn
            msisdn, imsi = get_subscription_data(diameter_message.message)
            subscriber = subscribers.get_subscriber(msisdn)
            # if subscriber does not exist, we create a new one
            if not subscriber:
                new_subscriber = Subscriber(msisdn, imsi)
                subscribers.add_subscriber(new_subscriber)
            subscriber = subscribers.get_subscriber(msisdn)
            # create a new gx session
            session_id = diameter_message.get_avp("Session-Id")
            framed_ip = diameter_message.get_avp("Framed-IP-Address")
            gx_session = GxSession(session_id, framed_ip)
            gx_session.add_message(diameter_message)
            gx_sessions.add_session(subscriber, gx_session)
        elif diameter_message_name == "AAR":
            session_id = diameter_message.get_avp("Session-Id")
            # in the aar, we get the subscriber from the framed_ip address used in the ccri
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                framed_ip = diameter_message.get_avp("Framed-IP-Address")
                subscriber = gx_sessions.get_subscriber_by_framed_ip(framed_ip)
                if not subscriber:
                    logging.error(f"Subscriber not found in diameter message {diameter_message_name} with framed ip {framed_ip}")
                    print(message)
                    continue
                # create new rx session with reference to gx session id with same framed ip
                gx_session = gx_sessions.get_session_by_framed_ip(framed_ip)
                rx_session = RxSession(session_id, gx_session, subscriber.msisdn)
                gx_session.add_rx_session(rx_session)
                rx_sessions.add_session(rx_session)
            # add the message to the new or existing rx session
            rx_session.add_message(diameter_message)
        elif diameter_message_name == "CCR-U" or diameter_message_name == "CCR-T" or diameter_message_name == "RAR" or diameter_message_name == "RAA":
            # get the subscriber through the gx session id
            session_id = diameter_message.get_avp("Session-Id")
            subscriber = gx_sessions.get_subscriber_by_session_id(session_id)
            if not subscriber:
                logging.error(f"Subscriber not found in diameter message {diameter_message_name} with session id {session_id}")
                print(message)
                continue
            # get the gx_session object and add the message
            gx_session = gx_sessions.get_session_by_session_id(session_id)
            gx_session.add_message(diameter_message)
        elif diameter_message_name == "CCA-I" or diameter_message_name == "CCA-U" or diameter_message_name == "CCA-T":
            session_id = diameter_message.get_avp("Session-Id")
            subscriber = gx_sessions.get_subscriber_by_session_id(session_id)
            if not subscriber:
                logging.error(f"Subscriber not found in diameter message {diameter_message_name} with session id {session_id}")
                print(message)
                continue
            # get the gx_session object, add the message and start/close the session depending on the message
            gx_session = gx_sessions.get_session_by_session_id(session_id)
            gx_session.add_message(diameter_message)
            if diameter_message_name == "CCA-I":
                gx_session.start_session(diameter_message)
            elif diameter_message_name == "CCA-T":
                gx_session.end_session(diameter_message)
        elif diameter_message_name == "AAA" :
            # in the aaa, get the rx_session from the rx session id, then get the subscriber from the gx session id associated
            session_id = diameter_message.get_avp("Session-Id")
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.start_session(diameter_message)
            rx_session.add_message(diameter_message)
        elif diameter_message_name == "STR" or diameter_message_name == "STA":
            # in the str/sta, we get the rx_session from the rx session id and add the message
            session_id = diameter_message.get_avp("Session-Id")
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.add_message(diameter_message)
        elif diameter_message_name == "ASR" or diameter_message_name == "ASA":
            # in the asr/asa, we get the rx_session from the rx session id and add the message
            session_id = diameter_message.get_avp("Session-Id")
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.add_message(diameter_message)
        else:
            logging.error(f"Message {diameter_message_name} not identified")
            print(message)
            continue
    return gx_sessions


class QosInformation:
#     # holds values of diameter.APN-Aggregate-Max-Bitrate-UL, diameter.APN-Aggregate-Max-Bitrate-DL, diameter.QoS-Class-Identifier
    def __init__(self, apn_aggregate_max_bitrate_ul, apn_aggregate_max_bitrate_dl, qos_class_identifier):
        self.apn_aggregate_max_bitrate_ul = apn_aggregate_max_bitrate_ul
        self.apn_aggregate_max_bitrate_dl = apn_aggregate_max_bitrate_dl
        self.qos_class_identifier = qos_class_identifier

    def __eq__(self, other):
        return self.apn_aggregate_max_bitrate_ul == other.apn_aggregate_max_bitrate_ul and self.apn_aggregate_max_bitrate_dl == other.apn_aggregate_max_bitrate_dl and self.qos_class_identifier == other.qos_class_identifier
    
    def __str__(self):
        return f"apn_aggregate_max_bitrate_ul: {self.apn_aggregate_max_bitrate_ul}, apn_aggregate_max_bitrate_dl: {self.apn_aggregate_max_bitrate_dl}, qos_class_identifier: {self.qos_class_identifier}"

def get_rat_type(diameter_message):
    rat_type = diameter_message.get_avp("RAT-Type")
    return rat_type

def get_ip_can_type(diameter_message):
    ip_can_type = diameter_message.get_avp("IP-CAN-Type")
    return ip_can_type

def get_event_triggers(diameter_message):
    event_triggers = diameter_message.get_avp("Event-Trigger")
    return event_triggers

def explain_gx_session(subscriber, gx_session):
    # for now we will just log messages for each diameter message
    for message_pair in gx_session.messages_pairs_tuples:
        # get the result_code from the answer
        result_code = message_pair[1].get_avp("Result-Code")
        if result_code != "2001":
            logging.error(f"{subscriber.msisdn} received error code {result_code} in {message_pair[1].message_name}")
        # first find the CCR-I/CCA-I pair
        if message_pair[0].message_name == "CCR-I" and message_pair[1].message_name == "CCA-I":
            explanation_string = f"{subscriber.msisdn} started session,"
            # get the ip_can_type and rat_type from the CCR-I
            ccr_i = message_pair[0]
            cca_i = message_pair[1]
            ip_can_type = get_ip_can_type(ccr_i)
            rat_type = get_rat_type(ccr_i)
            explanation_string += f"with {ip_can_type} and {rat_type},"
            # get qos information from the CCR-I and match with qos information in the CCA-I
            ccr_i_qos_information = QosInformation(ccr_i.get_avp("APN-Aggregate-Max-Bitrate-UL"), ccr_i.get_avp("APN-Aggregate-Max-Bitrate-DL"), ccr_i.get_avp("QoS-Class-Identifier"))
            cca_i_qos_information = QosInformation(cca_i.get_avp("APN-Aggregate-Max-Bitrate-UL"), cca_i.get_avp("APN-Aggregate-Max-Bitrate-DL"), cca_i.get_avp("QoS-Class-Identifier"))
            if ccr_i_qos_information != cca_i_qos_information:
                logging.error(f"{subscriber.msisdn},QoS requested was not granted by PCRF")
            # get the event triggers from the CCA-I
            event_triggers = get_event_triggers(message_pair[1])
            if event_triggers:
                explanation_string += f"with event triggers {event_triggers}"
            logging.info(explanation_string)
            # logging.info(f"{subscriber.msisdn} started session with {ip_can_type} and {rat_type} with event triggers {event_triggers}")
        elif message_pair[0].message_name == "CCR-U" and message_pair[1].message_name == "CCA-U":
            # get the event triggers that triggered the updated
            explanation_string = f"{subscriber.msisdn} updated session,"
            event_triggers = message_pair[0].get_avp("Event-Trigger")
            if event_triggers:
                explanation_string += f"event triggers {event_triggers}"
            logging.info(explanation_string)
        elif message_pair[0].message_name == "CCR-T" and message_pair[1].message_name == "CCA-T":
            # get the diameter.Termination-Cause
            termination_cause = message_pair[0].get_avp("Termination-Cause")
            logging.info(f"{subscriber.msisdn} terminated session with termination cause {termination_cause}")


def print_gx_session(subscriber, gx_session):
    for message in gx_session.messages:
        if message.is_request() and message.message_name != "RAR":
            if message.message_name == "CCR-I":
                logging.info(f"{subscriber.msisdn},{message},{gx_session.framed_ip}")
            else:
                logging.info(f"{subscriber.msisdn},{message}")
        elif message.message_name == "RAA":
            logging.info(f"{subscriber.msisdn},{message}")

def debug_gx_session(subscriber, gx_session):
    for message in gx_session.messages:
        logging.info(f"{subscriber.msisdn},{message},{message.fields}")



if __name__ == "__main__":
    # tshark_command = TsharkCommand("volte_4G_to_3G.cap", [10000, 20000])
    tshark_command = TsharkCommand("0706.pcap", [31009, 31115])
    # tshark_command = TsharkCommand("prueba_volte_20221109_5.pcap", [4000, 3880])
    subscribers = Subscribers()

    tshark_output = tshark_command.run(base_filter, all_fields)
    gx_sessions = parse_tshark_output(tshark_output, subscribers)
    rx_sessions = gx_sessions.rx_sessions

    # tshark_output = tshark_command.run_new(base_filter)
    # logging.info(f"tshark output: {tshark_output}")
    # tshark_output is a json string, make it into a list of dictionaries
    # tshark_output = json.loads(tshark_output)
    # gx_sessions = parse_tshark_output_new(tshark_output, subscribers)
    # rx_sessions = gx_sessions.rx_sessions

    for subscriber in subscribers.get_subscribers():
        if subscriber.gx_sessions:
            # get last gx_session for each subscriber
            # for gx_session in subscriber.gx_sessions:
            gx_session = subscriber.gx_sessions[-1]
            debug_gx_session(subscriber, gx_session)

    # for subscriber in subscribers.get_subscribers():
    #     if subscriber.gx_sessions:
    #         gx_session = subscriber.gx_sessions[-1]
    #         explain_gx_session(subscriber, gx_session)