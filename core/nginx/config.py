#!/usr/bin/python3

import os
import logging as log
import sys
from mailustart import resolve, convert

log.basicConfig(stream=sys.stderr, level=os.environ.get("LOG_LEVEL", "WARNING"))

# Get the first DNS server
with open("/etc/resolv.conf") as handle:
    content = handle.read().split()
    os.environ["RESOLVER"] = content[content.index("nameserver") + 1]

os.environ["HOST_WEBMAIL"] = resolve(os.environ.get("HOST_WEBMAIL", "webmail"))
os.environ["HOST_ADMIN"] = resolve(os.environ.get("HOST_ADMIN", "admin"))
os.environ["HOST_WEBDAV"] = resolve(os.environ.get("HOST_WEBDAV", "webdav:5232"))
os.environ["HOST_ANTISPAM"] = resolve(os.environ.get("HOST_ANTISPAM", "antispam:11334"))

# TLS configuration
cert_name = os.getenv("TLS_CERT_FILENAME", default="cert.pem")
keypair_name = os.getenv("TLS_KEYPAIR_FILENAME", default="key.pem")
os.environ["TLS"] = {
    "cert": ("/certs/%s" % cert_name, "/certs/%s" % keypair_name),
    "letsencrypt": ("/certs/letsencrypt/live/mailu/fullchain.pem",
        "/certs/letsencrypt/live/mailu/privkey.pem"),
    "mail": ("/certs/%s" % cert_name, "/certs/%s" % keypair_name),
    "mail-letsencrypt": ("/certs/letsencrypt/live/mailu/fullchain.pem",
        "/certs/letsencrypt/live/mailu/privkey.pem"),
    "notls": None
}[os.environ["TLS_FLAVOR"]]

if os.environ["TLS"] and not all(os.path.exists(file_path) for file_path in os.environ["TLS"]):
    print("Missing cert or key file, disabling TLS")
    os.environ["TLS_ERROR"] = "yes"

# Build final configuration paths
convert("/conf/tls.conf", "/etc/nginx/tls.conf")
convert("/conf/proxy.conf", "/etc/nginx/proxy.conf")
convert("/conf/nginx.conf", "/etc/nginx/nginx.conf")
if os.path.exists("/var/run/nginx.pid"):
    os.system("nginx -s reload")
