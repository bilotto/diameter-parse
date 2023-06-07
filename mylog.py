import logging

with open("output.log", "w") as f:
    f.write("")

DEBUG_MODE = True

# format = "%(levelname)s,%(asctime)s,%(funcName)s,%(threadName)s,%(message)s"
# format = "%(levelname)s,%(funcName)s,%(message)s"
format = "%(message)s"

if not DEBUG_MODE:
    logging.basicConfig(format=format,
                        # filename='/var/log/cron.log',
                        # filemode='a',
                        level=logging.INFO,
                        datefmt="%Y-%m-%dT%H:%M:%S",
                        handlers=[
                            # logging.FileHandler("/var/log/cron.log"),
                            # logging.FileHandler("/mnt/grdwhprdsftpsa05/FW_EMM/sa_log.log"),
                            logging.StreamHandler()
                        ])
else:
    logging.basicConfig(format=format,
                        level=logging.DEBUG,
                        datefmt="%Y-%m-%dT%H:%M:%S",
                        handlers=[
                            logging.FileHandler("output.log"),
                            logging.StreamHandler()
                        ])
