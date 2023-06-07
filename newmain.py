from mylog import logging
import pyshark

if __name__ == "__main__":
    base_filter = "diameter && !(diameter.cmd.code == 280) && !(diameter.cmd.code == 257)"
    # Read the pcap file
    cap = pyshark.FileCapture('prueba_volte_20221109_5.pcap', display_filter=base_filter)
    # Iterate over each packet in the capture
    for pkt in cap:
        # Check if the packet has the DIAMETER layer
        if hasattr(pkt, 'diameter'):

            # Log the start of a new Diameter message
            logging.info("Start of a new Diameter message")
            logging.info(f"{pkt.diameter}")

            # Print all fields in the DIAMETER layer
            for field in pkt.diameter.field_names:
                logging.info(f"{field}: {pkt.diameter.get_field_value(field)}")

            # Log the end of the Diameter message
            logging.info("End of Diameter message")
            logging.info("-------------------------")