# Filename: diameter_messages.py
# Base thark filter for all diameter messages
base_filter = "diameter && !(diameter.cmd.code == 280) && !(diameter.cmd.code == 257)"
# Base thark filter for all diameter messages
ip_fields = ["ip.src", "ip.dst"]
frame_dields = ["frame.time_epoch", "frame.number", "frame.time"]
base_fields = ip_fields + frame_dields

diameter_core_fields = ["diameter.cmd.code", "diameter.Session-Id", "diameter.flags.request", "diameter.Framed-IP-Address", "diameter.Subscription-Id-Data", "diameter.CC-Request-Type", "diameter.CC-Request-Number", "diameter.Framed-IP-Address.IPv4"]

diameter_fields = ["diameter.RAT-Type", "diameter.3gpp.charging_rule_name", "diameter.Event-Trigger", "diameter.IP-CAN-Type", "diameter.Result-Code", "diameter.Error-Message", "diameter.Offline", "diameter.Online", "diameter.Called-Station-Id"]

new_fields = ["diameter.Charging-Rule-Base-Name", "diameter.PCC-Rule-Status", "diameter.Rule-Failure-Code", "diameter.Rating-Group", "diameter.Termination-Cause", "diameter.Abort-Cause",  "diameter.Session-Release-Cause"]

pcc_fields = ["diameter.Charging-Rule-Remove", "diameter.Charging-Rule-Install", "diameter.QoS-Information", "diameter.Charging-Rule-Report", "diameter.Usage-Monitoring-Information"]
usage_monitoring_fields = ["diameter.CC-Total-Octets", "diameter.Monitoring-Key", "diameter.Granted-Service-Unit"]
qos_fields = ["diameter.APN-Aggregate-Max-Bitrate-UL", "diameter.APN-Aggregate-Max-Bitrate-DL", "diameter.Max-Requested-Bandwidth-UL", "diameter.Max-Requested-Bandwidth-DL", "diameter.QoS-Class-Identifier"]

aar_fields_only = ["diameter.Media-Component-Number", "diameter.Media-Type", "diameter.Flow-Number", "diameter.Specific-Action", "diameter.Flow-Usage", "diameter.Rx-Request-Type", "diameter.Flow-Status"]

diameter_fields = diameter_fields + usage_monitoring_fields + aar_fields_only + new_fields + qos_fields

all_fields = base_fields + diameter_core_fields + diameter_fields + pcc_fields

aar_debug_fields = ["diameter.3gpp.af_charging_identifier", "diameter.SIP-Forking-Indication", "diameter.Required-Access-Info", "diameter.Flow-Description"]

from hosts import HOSTS, clusters

from mylog import logging
from avp_values import avp_values
from functions import *
import datetime

gx_messages = ["CCR-I", "CCA-I", "CCR-U", "CCA-U", "CCR-T", "CCA-T", "RAR", "RAA"]
rx_messages = ["AAR", "AAA", "ASR", "ASA", "STR", "STA"]

class DiameterMessage:
    def __init__(self, message):
        # logging.info(f"{message}")
        # layers
        if message.get('_source'):
            ip_layer = message.get('_source').get('layers').get('ip')
            diameter_layer = message.get('_source').get('layers').get('diameter')
            frame_layer = message.get('_source').get('layers').get('frame')
        else:
            ip_layer = message
            diameter_layer = message
            frame_layer = message
        self.message = diameter_layer
        self.fields = add_fields_if_exist(message, diameter_fields, {})
        # get fields from ip layer
        self.from_host = HOSTS.get(ip_layer.get('ip.src'), ip_layer.get('ip.src'))
        self.to_host = HOSTS.get(ip_layer.get('ip.dst'), ip_layer.get('ip.dst'))
        # get fields from diameter layer
        # self.diameter_request = int(diameter_layer.get('diameter.flags_tree').get("diameter.flags.request"))
        self.diameter_request = int(diameter_layer.get("diameter.flags.request"))
        self.diameter_code = int(diameter_layer.get('diameter.cmd.code'))
        # logging.info(f"{diameter_layer}")
        self.diameter_layer = None
        # new_diameter_layer = parse_diameter_layer(diameter_layer)
        # logging.info(f"{new_diameter_layer}")
        self.cc_request_type = self.get_avp('diameter.CC-Request-Type')

        # logging.debug(f"Message: {self.message}")
        self.message_name = name_diameter_message(self.diameter_code, self.diameter_request, self.cc_request_type)
        # get fields from frame layer
        self.frame_time_epoch = frame_layer.get('frame.time_epoch')
        self.frame_number = frame_layer.get('frame.number')
        self.time = self.frame_time_epoch
        # self.time = self.get_time()
        self.time_other_format = datetime.datetime.fromtimestamp(float(self.time)).strftime('%Y-%m-%d %H:%M:%S')
        self.cluster = clusters.get_cluster_name_by_host(self.from_host) or clusters.get_cluster_name_by_host(self.to_host)
        #

    def __repr__(self) -> str:
        # return f"{self.time_other_format},{self.from_host},{self.to_host},{self.message_name},{self.fields}"
        return f"{self.time_other_format},{self.to_host},{self.message_name}"
        # return f"{self.time_other_format},{self.message_name},{self.fields}"
        # return f"{self.time_other_format},{self.message_name}"
    

    def get_time(self):
        frame_time = self.message.get('frame.time_epoch')
        return frame_time
    
    def is_gx(self):
        return self.message_name in gx_messages
    
    def is_rx(self):
        return self.message_name in rx_messages
            
    def get_avp(self, avp_name):
        if not "diameter." in avp_name:
            avp_name = "diameter." + avp_name
        if self.fields.get(avp_name):
            return self.fields.get(avp_name)
        else:
            return self.message.get(avp_name)
        
    def is_request(self):
        return self.diameter_request
    
def parse_diameter_layer(diameter_layer, new_diameter_layer=None):
    if new_diameter_layer is None:
        new_diameter_layer = {}

    # check the avp list in the avp_tree field
    if 'diameter.avp_tree' in diameter_layer:
        for avp_dict in diameter_layer.get('diameter.avp_tree'):
            # the avp_dict can have another diameter.avp_tree field, and so on
            if isinstance(avp_dict, dict):
                keys_set = set(avp_dict.keys())
                for key, value in avp_dict.items():
                    if ".avp." in key:
                        continue
                    if "diameter." not in key:
                        continue
                    # Check if there is a _tree variant of the key in the set.
                    # If it does not exist, add key to the new_diameter_layer dictionary.
                    if f'{key}_tree' not in keys_set:
                        if "tree" not in key:
                            if not new_diameter_layer.get(key):
                                new_diameter_layer[key] = value
                            else:
                                # create a list with the current value
                                current_value = new_diameter_layer[key]
                                new_diameter_layer[key] = []
                                new_diameter_layer[key].append(current_value)
                                new_diameter_layer[key].append(value)
                    # check if this is another 'diameter.avp_tree' to parse
                    if key.endswith('_tree'):
                        # call function recursively to parse this 'diameter.avp_tree'
                        parse_diameter_layer(value, new_diameter_layer)
            else:
                logging.debug(f"Error: {avp_dict}")


    return new_diameter_layer





def add_fields_if_exist(line, fields, output):
    for field in fields:
        if line.get(field):
            if not "," in line.get(field):
                if avp_values.get(field):
                    output[field] = avp_values.get(field).get(line.get(field), field)
                else:
                    output[field] = line.get(field)
            else:
                # multiple values in the same field
                if not avp_values.get(field):
                    output[field] = line.get(field)
                else:
                    for value in line.get(field).split(","):
                        if not output.get(field):
                            output[field] = avp_values.get(field).get(value, value)
                        else:
                            output[field] += "," + str(avp_values.get(field).get(value, value))
    return output

def name_diameter_message(diameter_code, diameter_request, cc_request_type):
    # logging.debug(f"diameter_code: {diameter_code}, diameter_request: {diameter_request}, cc_request_type: {cc_request_type}")
    if diameter_code == 272:
        if diameter_request:
            if cc_request_type == '1':
                message = "CCR-I"
            elif cc_request_type == '2':
                message = "CCR-U"
            elif cc_request_type == '3':
                message = "CCR-T"
        else:
            if cc_request_type == '1':
                message = "CCA-I"
            elif cc_request_type == '2':
                message = "CCA-U"
            elif cc_request_type == '3':
                message = "CCA-T"
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
        message = "Unknown"
    return message

