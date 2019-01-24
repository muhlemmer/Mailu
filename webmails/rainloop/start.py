#!/usr/bin/python3

import os
import shutil
import logging as log
import sys
from mailustart import resolve, convert

log.basicConfig(stream=sys.stderr, level=os.environ.get("LOG_LEVEL", "WARNING"))

# Actual startup script
os.environ["FRONT_ADDRESS"] = resolve(os.environ.get("FRONT_ADDRESS", "front"))
os.environ["IMAP_ADDRESS"] = resolve(os.environ.get("IMAP_ADDRESS", "imap"))

os.environ["MAX_FILESIZE"] = str(int(int(os.environ.get("MESSAGE_SIZE_LIMIT"))*0.66/1048576))

base = "/data/_data_/_default_/"
shutil.rmtree(base + "domains/", ignore_errors=True)
os.makedirs(base + "domains", exist_ok=True)
os.makedirs(base + "configs", exist_ok=True)

convert("/default.ini", "/data/_data_/_default_/domains/default.ini")
convert("/config.ini", "/data/_data_/_default_/configs/config.ini")
convert("/php.ini", "/usr/local/etc/php/conf.d/rainloop.ini")

os.system("chown -R www-data:www-data /data")

os.execv("/usr/local/bin/apache2-foreground", ["apache2-foreground"])

