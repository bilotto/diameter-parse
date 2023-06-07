import subprocess
from mylog import logging
from diameter_messages import HOSTS

class TsharkCommand:
    def __init__(self, file, ports=None):
        self.file = file
        self.ports = ports
        
    def get_ports(self):
        command = ""
        for port in self.ports:
            command += f"-d tcp.port=={port},diameter "
        return command
    
    def get_fields(self, fields):
        command = ""
        for field in fields:
            command += f"-e {field} "
        return command
    
    def generate(self, filter, fields, output_file=None):
        if not output_file:
            command_template = f"tshark -r {self.file} {self.get_ports()} -Y '{filter}' -T fields {self.get_fields(fields)}"
            return command_template
        else:
            command_template = f"tshark -r {self.file} {self.get_ports()} -Y '{filter}' -T fields {self.get_fields(fields)} -w {output_file}"
            return command_template


    def run(self, filter, fields, output_file=None):
        tshark_command = self.generate(filter, fields, output_file)
        logging.info(f"Running tshark command: {tshark_command}")
        tshark_output = subprocess.check_output(tshark_command, shell=True).decode("utf-8")
        output_list_of_dicts = []
        output = tshark_output.split("\n")
        for line in output:
            if line == "":
                continue
            # Create dictionary placeholder for each field
            fields_dict = {}
            for field in fields:
                fields_dict[field] = None
            # Fill dictionary with values
            params = line.split("\t")
            for i in range(len(params)):
                fields_dict[fields[i]] = params[i]
            # # Append dictionary to list            
            if not HOSTS.get(fields_dict.get("ip.src")) and not HOSTS.get(fields_dict.get("ip.dst")):
                continue
            output_list_of_dicts.append(fields_dict)
        return output_list_of_dicts

    def run_new(self, filter, output_file=None):
        tshark_command = f"tshark -r {self.file} {self.get_ports()} -Y '{filter}' -T json --no-duplicate-keys"
        logging.info(f"Running tshark command: {tshark_command}")
        tshark_output = subprocess.check_output(tshark_command, shell=True).decode("utf-8")
        return tshark_output


def hex_to_ip(hex_ip):
    # check if the input is a string and it has exactly 8 characters
    if not isinstance(hex_ip, str) or len(hex_ip) != 8:
        raise ValueError("Input must be an 8-character hexadecimal string")
    # split the hexadecimal string into 4 parts
    ip_parts = [hex_ip[i:i+2] for i in range(0, 8, 2)]
    # convert each hexadecimal part to decimal and join them with dots
    ip = ".".join(str(int(part, 16)) for part in ip_parts)
    return ip


# from datetime import datetime

# def convert_time_format(s):
#     # split timestamp and timezone
#     timestamp, timezone = s.rsplit(" ", 1)
#     # trim fractional seconds to microseconds
#     timestamp = timestamp[:timestamp.rindex('.')+7]
#     # create datetime object from string
#     dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S.%f")
#     # create new string from datetime object
#     new_s = dt.strftime("%H:%M:%S.%f")
#     return new_s

# def convert_time_format_v2(s):
#     # split timestamp and timezone
#     timestamp, timezone = s.rsplit(" ", 1)
#     # trim fractional seconds to milliseconds
#     timestamp = timestamp[:timestamp.rindex('.')+4]
#     # create datetime object from string
#     dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S.%f")
#     # create new string from datetime object
#     new_s = dt.strftime("%b %d, %Y %H:%M:%S.%f")[:-3]
#     return new_s

# def convert_time_format_v3(s):
#     # split timestamp and timezone
#     timestamp, timezone = s.rsplit(" ", 1)
#     # trim fractional seconds to seconds
#     timestamp = timestamp[:timestamp.rindex('.')]
#     # create datetime object from string
#     dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S")
#     # create new string from datetime object
#     new_s = dt.strftime("%Y-%m-%d %H:%M:%S")
#     return new_s


# def convert_to_timestamp(s):
#     # split timestamp and timezone
#     timestamp, timezone = s.rsplit(" ", 1)
#     # trim fractional seconds to seconds
#     timestamp = timestamp[:timestamp.rindex('.')]
#     # create datetime object from string
#     dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S")
#     # convert datetime object to timestamp
#     ts = dt.timestamp()
#     return int(ts)

# def convert_to_timestamp_with_ms(s):
#     # split timestamp and timezone
#     timestamp, timezone = s.rsplit(" ", 1)

#     # trim fractional seconds to milliseconds
#     timestamp = timestamp[:timestamp.rindex('.')+4]

#     # create datetime object from string
#     dt = datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S.%f")

#     # convert datetime object to timestamp with milliseconds
#     ts = round(dt.timestamp(), 3)

#     return ts

