# Filename: diameter_messages.py
# Base thark filter for all diameter messages
base_filter = "diameter && !(diameter.cmd.code == 280) && !(diameter.cmd.code == 257)"
# Base thark filter for all diameter messages
base_fields = ["frame.time", "ip.src", "ip.dst", "frame.time_epoch", "frame.number"]

diameter_core_fields = ["diameter.cmd.code", "diameter.Session-Id", "diameter.flags.request", "diameter.Framed-IP-Address", "diameter.Subscription-Id-Data", "diameter.CC-Request-Type"]

diameter_fields = ["diameter.RAT-Type", "diameter.3gpp.charging_rule_name", "diameter.Event-Trigger", "diameter.IP-CAN-Type", "diameter.Framed-IP-Address.IPv4", "diameter.Result-Code", "diameter.Max-Requested-Bandwidth-DL", "diameter.Error-Message", "diameter.Offline", "diameter.Online"]

all_fields = base_fields + diameter_core_fields + diameter_fields

aar_fields_only = ["diameter.Media-Component-Number", "diameter.Media-Type", "diameter.Flow-Number", "diameter.Specific-Action", "diameter.Flow-Usage", "diameter.Rx-Request-Type", "diameter.Flow-Status"]

aar_debug_fields = ["diameter.3gpp.af_charging_identifier", "diameter.SIP-Forking-Indication", "diameter.Required-Access-Info", "diameter.Flow-Description"]

diameter_fields = diameter_fields + aar_fields_only + aar_debug_fields

binary_fields = ["diameter.Charging-Rule-Remove", "diameter.Charging-Rule-Install"]

all_fields = all_fields + aar_fields_only + binary_fields

from hosts import HOSTS, clusters

from mylog import logging
from avp_values import avp_values
from functions import *
import datetime

class DiameterMessage:
    def __init__(self, message):
        self.message = message
        self.message_name = self.identify()
        #
        self.session_id = message.get('diameter.Session-Id')
        self.time = self.get_time()
        self.request = message.get('diameter.flags.request')
        self.fields = add_fields_if_exist(message, diameter_fields, {})
        self.from_host = HOSTS.get(message.get('ip.src'), message.get('ip.src'))
        self.to_host = HOSTS.get(message.get('ip.dst'), message.get('ip.dst'))
        self.time_other_format = datetime.datetime.fromtimestamp(float(self.time)).strftime('%Y-%m-%d %H:%M:%S')
        self.cluster = clusters.get_cluster_name_by_host(message.get('ip.src')) or clusters.get_cluster_name_by_host(message.get('ip.dst'))

    def __repr__(self) -> str:
        return f"{self.time_other_format},{self.from_host},{self.to_host},{self.message_name},{self.fields}"
        # return f"{self.time_other_format},{self.to_host},{self.message_name}"
    

    def get_time(self):
        frame_time = self.message.get('frame.time_epoch')
        return frame_time

    def identify(self):
        message_name = identify_diameter_message(self.message)
        return message_name
    
    def is_voice_call(self):
        if self.message.get('diameter.Media-Type'):
            return True
        
    def get_avp(self, avp):
        # return self.message.get(avp)
        return self.fields.get(avp)
    
    def parse_message(self):
        self.pcc_rules()


    def event_triggers(self):
        event_triggers = []
        if self.message.get('diameter.Event-Trigger'):
            event_triggers = self.message.get('diameter.Event-Trigger').split(",")
        return event_triggers

    def pcc_rules(self):
        rules = []
        # check if we are installing or removing rules
        if self.message.get('diameter.Charging-Rule-Install'):
            # we are installing rules, get the charging_rule_name, which is a list comma separated
            charging_rule_name = self.message.get('diameter.3gpp.charging_rule_name')
            # get the list of rules
            rules = charging_rule_name.split(",")
            logging.info(f"{self.time},Installing rules {rules}")
            return True, rules
        elif self.message.get('diameter.Charging-Rule-Remove'):
            # do the same
            charging_rule_name = self.message.get('diameter.3gpp.charging_rule_name')
            rules = charging_rule_name.split(",")
            logging.info(f"{self.time},Removing rules {rules}")
            return False, rules
        else:
            return None, None
        

        
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
                            output[field] += "," + str(avp_values.get(field).get(value))
    return output


    
def identify_diameter_message(message):
    diameter_code = int(message['diameter.cmd.code'])
    diameter_request = int(message['diameter.flags.request'])
    if diameter_code == 272:
        diameter_cc_request_type = message.get('diameter.CC-Request-Type')
        if diameter_request:
            if diameter_cc_request_type == '1':
                message = "CCR_I"
            elif diameter_cc_request_type == '2':
                message = "CCR_U"
            elif diameter_cc_request_type == '3':
                message = "CCR_T"
        else:
            if diameter_cc_request_type == '1':
                message = "CCA_I"
            elif diameter_cc_request_type == '2':
                message = "CCA_U"
            elif diameter_cc_request_type == '3':
                message = "CCA_T"
    elif diameter_code == 258:
        if diameter_request:
            message = "RAR"
        else:
            message = "RAA"
    elif diameter_code == 265:
        if diameter_request:
            message = "AAR"
        else:
            message = "AAA"
    elif diameter_code == 275:
        if diameter_request:
            message = "STR"
        else:
            message = "STA"
    elif diameter_code == 274:
        if diameter_request:
            message = "ASR"
        else:
            message = "ASA"
    else:
        print(message)
    return message

