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


def add_fields_if_exist(line, fields, output):
    for field in fields:
        if line.get(field):
            if not "," in line.get(field):
                if avp_values.get(field):
                    output[field] = avp_values.get(field).get(line.get(field))
                else:
                    output[field] = line.get(field)
            else:
                # multiple values in the same field
                if not avp_values.get(field):
                    output[field] = line.get(field)
                else:
                    for value in line.get(field).split(","):
                        if not output.get(field):
                            output[field] = avp_values.get(field).get(value)
                        else:
                            output[field] += "," + avp_values.get(field).get(value)
    return output


def parse_tshark_output(tshark_output, subscribers):
    rx_sessions = RxSessions()
    gx_sessions = GxSessions(subscribers, rx_sessions)
    
    for message in tshark_output:
        diameter_message = DiameterMessage(message)
        diameter_message_name = diameter_message.identify()
        if diameter_message_name == "CCR_I":
            # in the ccri, we get the subscriber from the msisdn
            msisdn, imsi = get_subscription_data(diameter_message.message)
            subscriber = subscribers.get_subscriber(msisdn)
            # if subscriber does not exist, we create a new one
            if not subscriber:
                new_subscriber = Subscriber(msisdn, imsi)
                subscribers.add_subscriber(new_subscriber)
            subscriber = subscribers.get_subscriber(msisdn)
            # create a new gx session
            session_id = get_session_id(diameter_message.message)
            framed_ip = get_framed_ip(diameter_message.message)
            gx_session = GxSession(session_id, framed_ip)
            gx_session.add_message(diameter_message)
            gx_sessions.add_session(subscriber, gx_session)
        elif diameter_message_name == "AAR":
            session_id = get_session_id(diameter_message.message)
            # in the aar, we get the subscriber from the framed_ip address used in the ccri
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                framed_ip = get_framed_ip(diameter_message.message)
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
        elif diameter_message_name == "CCR_U" or diameter_message_name == "CCR_T" or diameter_message_name == "RAR" or diameter_message_name == "RAA":
            # get the subscriber through the gx session id
            session_id = get_session_id(diameter_message.message)
            subscriber = gx_sessions.get_subscriber_by_session_id(session_id)
            if not subscriber:
                logging.error(f"Subscriber not found in diameter message {diameter_message_name} with session id {session_id}")
                print(message)
                continue
            # get the gx_session object and add the message
            gx_session = gx_sessions.get_session_by_session_id(session_id)
            gx_session.add_message(diameter_message)
        elif diameter_message_name == "CCA_I" or diameter_message_name == "CCA_U" or diameter_message_name == "CCA_T":
            session_id = get_session_id(diameter_message.message)
            subscriber = gx_sessions.get_subscriber_by_session_id(session_id)
            if not subscriber:
                logging.error(f"Subscriber not found in diameter message {diameter_message_name} with session id {session_id}")
                print(message)
                continue
            # get the gx_session object, add the message and start/close the session depending on the message
            gx_session = gx_sessions.get_session_by_session_id(session_id)
            gx_session.add_message(diameter_message)
            if diameter_message_name == "CCA_I":
                gx_session.start_session(diameter_message)
            elif diameter_message_name == "CCA_T":
                gx_session.end_session(diameter_message)
        elif diameter_message_name == "AAA" :
            # in the aaa, get the rx_session from the rx session id, then get the subscriber from the gx session id associated
            session_id = get_session_id(diameter_message.message)
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.start_session(diameter_message)
            rx_session.add_message(diameter_message)
        elif diameter_message_name == "STR":
            # in the str, we get the rx_session from the rx session id and add the message
            session_id = get_session_id(diameter_message.message)
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.add_message(diameter_message)
        elif diameter_message_name == "STA":
            # in the sta, we get the rx_session from the rx session id and add the message
            session_id = get_session_id(diameter_message.message)
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.add_message(diameter_message)
            rx_session.end_session(diameter_message)
        elif diameter_message_name == "ASR" or diameter_message_name == "ASA":
            # in the asr/asa, we get the rx_session from the rx session id and add the message
            session_id = get_session_id(diameter_message.message)
            rx_session = rx_sessions.get_session_by_session_id(session_id)
            if not rx_session:
                continue
            rx_session.add_message(diameter_message)
        else:
            logging.error(f"Message {diameter_message_name} not identified")
            print(message)
            continue
    return gx_sessions


def explain_gx_session(subscriber, gx_session):
    messages = gx_session.messages
    for message in messages:
        # first, let's check the message type. in the ccr_i, lets get the RAT-Type and IP-CAN-Type
        # in the cca_i, check the event-trigger installed
        # in the rar, check the pcc rules
        if message.message_name == "CCR_I":
            rat_type = message.get_avp("diameter.RAT-Type")
            ip_can_type = message.get_avp("diameter.IP-CAN-Type")
            to_host = message.to_host
            # Subscriber msisdn started session on to_host with ip_can_type and rat_type
            logging.info(f"{subscriber.msisdn},{message.message_name},{to_host},{ip_can_type},{rat_type}")

        # elif message.message_name == "CCA_I":
        #     event_trigger = message.get_avp("diameter.Event-Trigger")
        #     # triggers are comma separated
        #     triggers = event_trigger.split(",")
        #     logging.info(f"{subscriber.msisdn},{message.message_name},{triggers}")
        # else:
        #     logging.info(f"{subscriber.msisdn},{message.message_name},{message.fields}")


if __name__ == "__main__":
    # first, clean the log file output.log
    with open("output.log", "w") as f:
        f.write("")
    # tshark_command = TsharkCommand("output.pcap", [31009, 31115])
    # tshark_command = TsharkCommand("volte_4G_to_3G.cap", [10000, 20000])
    # tshark_command = TsharkCommand("2405.pcap", [31009, 31115])
    tshark_command = TsharkCommand("prueba_251022.pcap", [4000, 3880])
    subscribers = Subscribers()
    #pospago
    subscriber1 = Subscriber("56950018795", "730030540816229")
    subscriber2 = Subscriber("56986124800", "730030540816203")
    #prepago
    subscriber3 = Subscriber("56973401557", "730030540816207")
    subscriber4 = Subscriber("56973179039", "730030540816206")
    subscribers.add_subscriber(subscriber1)
    subscribers.add_subscriber(subscriber2)
    subscribers.add_subscriber(subscriber3)
    subscribers.add_subscriber(subscriber4)
    subscribers.add_subscriber(Subscriber("56946117399","730030540816245"))
    subscribers.add_subscriber(Subscriber("56954225424","730030540816243"))

    tshark_output = tshark_command.run(base_filter, all_fields)

    gx_sessions = parse_tshark_output(tshark_output, subscribers)
    rx_sessions = gx_sessions.rx_sessions

    for subscriber in subscribers.get_subscribers():
        if subscriber.gx_sessions:
            # show only last gx_session for each subscriber
            gx_session = subscriber.gx_sessions[-1]
            # tshark_output = tshark_command.run(gx_session.tshark_filter, all_fields, f"{subscriber.msisdn}.pcap")
            
            session_binding = gx_session.session_binding
            if session_binding == False:
                logging.error(f"{subscriber},RxSession in a different cluster")
            for message in gx_session.messages:
                logging.info(f"{subscriber},{message}")
                # if message.message_name == "CCR_I" or message.message_name == "AAR" or message.message_name == "RAA":
                #     logging.info(f"{subscriber},{message}")
            # explain_gx_session(subscriber, gx_session)