import ipaddress
import json

ZIP2DMA = json.load(open('dma.json'))


def check_and_reformat_ip(ip):
    ipaddress.ip_address(ip)
    if ":" in ip:
        ip = ":".join(ip.split(":")[:4])
        if not ip.endswith(":"):
            return ip + "::"
        else:
            return ip + ":"
    return ip
